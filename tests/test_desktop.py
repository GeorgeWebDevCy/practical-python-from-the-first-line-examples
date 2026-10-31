"""Actual Tk widget tests. A working graphical display is required; no silent skips."""
from pathlib import Path
from tempfile import TemporaryDirectory
from threading import Event
import tkinter as tk
import unittest
from unittest.mock import patch

from examples.ch17.board import load_requests
from examples.ch19.timer import FocusTimer
from examples.ch19.first_window import build_window
from examples.ch20.tracker import RequestTracker
from examples.ch21.assistant_gui import PlanningAssistant
from examples.ch21.planning import PlannerError, offline_plan


class DesktopTests(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.root.withdraw()
        self.directory = TemporaryDirectory()
        self.path = Path(self.directory.name) / "requests.json"

    def tearDown(self):
        try:
            self.root.destroy()
        except tk.TclError:
            pass
        self.directory.cleanup()

    def test_first_window_button_changes_the_real_label_variable(self):
        message, button = build_window(self.root)
        self.assertEqual(message.get(), "Ready for a small experiment.")
        button.invoke()
        self.assertEqual(message.get(), "You pressed the button.")

    def test_timer_start_pause_resume_reset_and_completion(self):
        clock = [100.0]
        timer = FocusTimer(self.root, seconds=5, clock=lambda: clock[0])
        self.assertEqual(timer.display.get(), "00:05")
        timer.start_button.invoke()
        first_job = timer.job
        timer.start()
        self.assertEqual(timer.job, first_job)
        clock[0] = 102.25
        timer.tick()
        self.assertAlmostEqual(timer.remaining, 2.75)
        self.assertEqual(timer.display.get(), "00:03")
        timer.pause_button.invoke()
        self.assertFalse(timer.running)
        self.assertIsNone(timer.job)
        clock[0] = 200
        timer.start_button.invoke()
        self.assertAlmostEqual(timer.deadline, 202.75)
        clock[0] = 203
        timer.tick()
        self.assertEqual(timer.display.get(), "00:00")
        self.assertIn("complete", timer.status.get())
        self.assertFalse(timer.running)
        timer.reset_button.invoke()
        self.assertEqual(timer.remaining, 5)
        self.assertIsNone(timer.job)

    def test_timer_rejects_bad_duration_and_closes_scheduled_work(self):
        for value in (0, -1, True, 1.5):
            with self.subTest(value=value), self.assertRaises(ValueError):
                FocusTimer(self.root, value)
        timer = FocusTimer(self.root, 2)
        timer.start()
        timer.close()
        self.assertIsNone(timer.job)

    def test_tracker_real_widgets_persist_and_refresh(self):
        app = RequestTracker(self.root, self.path)
        self.assertFalse(self.path.exists())
        self.assertFalse(app.add())
        self.assertIn("Title", app.status.get())
        app.title_text.set("  Check the workshop inventory  ")
        app.add_button.invoke()
        self.assertEqual(load_requests(self.path)[0]["title"], "Check the workshop inventory")
        self.assertEqual(app.summary.get(), "1 open / 1 total")
        self.assertEqual(app.title_text.get(), "")
        app.complete_button.invoke()
        self.assertTrue(load_requests(self.path)[0]["done"])
        self.assertEqual(app.summary.get(), "0 open / 1 total")
        app.refresh()
        self.assertEqual(app.tree.item("1", "values")[1], "done")

    def test_tracker_failed_save_preserves_input_and_bad_storage(self):
        app = RequestTracker(self.root, self.path)
        self.assertFalse(app.complete())
        app.title_text.set("Keep my draft")
        with patch("examples.ch20.tracker.add_request", side_effect=OSError("disk unavailable")):
            self.assertFalse(app.add())
        self.assertEqual(app.title_text.get(), "Keep my draft")
        self.assertFalse(self.path.exists())
        self.path.write_text("malformed", encoding="utf-8")
        self.assertFalse(app.refresh())
        self.assertFalse(app.add())
        self.assertEqual(self.path.read_text(encoding="utf-8"), "malformed")

    def test_assistant_review_is_required_before_saving(self):
        app = PlanningAssistant(self.root, self.path)
        app.goal.set("Prepare a workshop")
        app.suggest_button.invoke()
        app.worker.join(timeout=3)
        self.assertFalse(app.worker.is_alive())
        app.poll()
        self.assertEqual(len(app.suggestions.get_children()), 3)
        self.assertFalse(self.path.exists())
        self.assertFalse(app.accept())
        app.suggestions.selection_set("1")
        app.accept_button.invoke()
        records = load_requests(self.path)
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0]["title"], "Choose one small step to try first")
        self.assertEqual(len(app.suggestions.get_children()), 2)
        self.assertFalse(records[0]["done"])

    def test_assistant_live_consent_empty_goal_and_failure(self):
        calls = []
        def failed(goal):
            calls.append(goal)
            raise PlannerError("Service temporarily unavailable.")
        app = PlanningAssistant(self.root, self.path, provider=failed, live=True)
        app.suggest()
        self.assertIsNone(app.worker)
        app.goal.set("Prepare a workshop")
        app.suggest()
        self.assertEqual(calls, [])
        self.assertIn("confirm", app.status.get())
        app.consent.set(True)
        app.suggest()
        app.worker.join(timeout=3)
        app.poll()
        self.assertEqual(calls, ["Prepare a workshop"])
        self.assertIn("unavailable", app.status.get())
        self.assertFalse(app.busy)
        self.assertFalse(self.path.exists())

    def test_close_during_worker_never_touches_destroyed_widgets(self):
        entered, release = Event(), Event()
        def delayed(goal):
            entered.set()
            release.wait(timeout=3)
            return offline_plan(goal)
        app = PlanningAssistant(self.root, self.path, provider=delayed)
        app.goal.set("Prepare a workshop")
        app.suggest()
        self.assertTrue(entered.wait(timeout=2))
        app.close()
        release.set()
        app.worker.join(timeout=3)
        self.assertFalse(app.worker.is_alive())
        self.assertTrue(app.closed)
        self.assertIsNone(app.job)
        self.assertFalse(self.path.exists())

    def test_invalid_provider_response_is_not_displayed_or_saved(self):
        app = PlanningAssistant(self.root, self.path, provider=lambda goal: [{"title": "x", "category": "unknown"}])
        app.goal.set("Prepare a workshop")
        app.suggest()
        app.worker.join(timeout=3)
        app.poll()
        self.assertEqual(app.suggestions.get_children(), ())
        self.assertFalse(self.path.exists())
