"""Behaviour checks for the chapter contracts and runnable command outputs."""
import contextlib
import importlib.util
import io
import json
from pathlib import Path
import subprocess
import sys
import unittest

from examples.verification import run_case

ROOT = Path(__file__).resolve().parents[1]


def load(relative):
    path = ROOT / relative
    spec = importlib.util.spec_from_file_location(path.stem, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def run_changed(relative, old, new):
    code = (ROOT / relative).read_text(encoding="utf-8")
    if code.count(old) != 1:
        raise AssertionError(f"Expected one replacement target: {old}")
    output = io.StringIO()
    with contextlib.redirect_stdout(output):
        exec(compile(code.replace(old, new), relative, "exec"), {})
    return output.getvalue()


class ChapterTests(unittest.TestCase):
    def test_all_documented_commands(self):
        cases = json.loads((ROOT / "examples/cases.json").read_text(encoding="utf-8"))["cases"]
        for case in cases:
            with self.subTest(script=case["script"]):
                run_case(case)

    def test_trip_changed_distance(self):
        self.assertEqual(run_changed("examples/ch02/trip.py", "distance_km = 18", "distance_km = 24"),
                         "Destination: Harbour\nTravel minutes: 120\nIncluding stop: 130\n")

    def test_input_cleaning_zero_and_rejected_text(self):
        path = ROOT / "examples/ch03/session.py"
        result = subprocess.run([sys.executable, str(path)], input="  Sam Lee  \n0\n",
                                capture_output=True, text=True, timeout=10)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, "Your name: Practice minutes: Plan for Sam Lee\nTotal including break: 5 minutes\n")
        for value in ("twenty", "2.5"):
            with self.subTest(value=value):
                result = subprocess.run([sys.executable, str(path)], input=f"Sam\n{value}\n",
                                        capture_output=True, text=True, timeout=10)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("ValueError", result.stderr)

    def test_decision_boundaries(self):
        for value, expected in [(-1, "Minutes cannot be negative."), (0, "No session planned."),
                                (1, "Review one example."), (19, "Review one example."),
                                (20, "Complete a practice exercise."), (21, "Complete a practice exercise.")]:
            with self.subTest(value=value):
                self.assertEqual(run_changed("examples/ch04/choose.py", "minutes = 20", f"minutes = {value}"), expected + "\n")

    def test_empty_sessions(self):
        result = run_changed("examples/ch06/weekly.py", "sessions = [15, 20, 10]", "sessions = []")
        self.assertEqual(result, "Weekly total: 0 minutes\nCountdown: 3\nCountdown: 2\nCountdown: 1\n")

    def test_travel_contract(self):
        travel = load("examples/ch07/travel.py").travel_minutes
        self.assertAlmostEqual(travel(18), 90)
        self.assertAlmostEqual(travel(0), 0)
        self.assertAlmostEqual(travel(18, speed_kmh=9), 120)
        for distance, speed in [(-1, 12), (18, 0), (18, -1)]:
            with self.subTest(distance=distance, speed=speed):
                with self.assertRaises(ValueError):
                    travel(distance, speed)

    def test_parse_minutes(self):
        parse = load("examples/ch08/durations.py").parse_minutes
        self.assertEqual(parse(" 25 "), 25)
        self.assertEqual(parse("0"), 0)
        for text in ("-2", "many", "2.5", ""):
            with self.subTest(text=text):
                with self.assertRaises(ValueError):
                    parse(text)
