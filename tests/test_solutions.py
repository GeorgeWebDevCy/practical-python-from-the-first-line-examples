from io import StringIO
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

from examples import solutions as s
from examples.ch12.organise import organise
from examples.ch13.report import SAMPLE
from test_projects import handler_for, serving


class SolutionTests(unittest.TestCase):
    def test_foundation_solutions(self):
        self.assertEqual(s.trip_estimate(), (120, 140))
        self.assertEqual(s.trip_estimate(stop_minutes=5), (120, 125))
        self.assertEqual(s.lesson_plan(" Alex ", "17"), ("Alex", 20))
        self.assertEqual(s.lesson_plan("Alex", "0"), ("Alex", 3))
        with self.assertRaises(ValueError):
            s.lesson_plan("Alex", "many")
        expected = ["Invalid hour", "Workshop closed", "Drop-offs accepted",
                    "Drop-offs accepted", "Workshop closed", "Invalid hour"]
        self.assertEqual([s.workshop_message(h) for h in (-1, 8, 9, 15, 16, 24)], expected)
        self.assertEqual(s.reading_plan(), ("loops", 20, 2, "No notes"))
        self.assertEqual(s.checklist([]), "Nothing to pack.")
        self.assertEqual(s.checklist(["water"]), "1. water")
        self.assertEqual(s.checklist(["water", "map"]), "1. water\n2. map")
        self.assertEqual(s.two_sessions(25, 10), (30, 15))

    def test_extended_classifier_with_apply(self):
        self.assertEqual(s.classify_with_data(Path("settings.JSON")), "data")
        self.assertEqual(s.classify_with_data(Path("note.txt")), "notes")
        with TemporaryDirectory() as folder:
            root = Path(folder)
            source = root / "in"
            source.mkdir()
            (source / "totals.csv").write_bytes(b"a,b\n1,2\n")
            (source / "old.csv").mkdir()
            with patch("examples.ch12.organise.classify", s.classify_with_data):
                organise(source, root / "out", apply=True)
            self.assertEqual((root / "out/data/totals.csv").read_bytes(), b"a,b\n1,2\n")
            self.assertTrue((source / "totals.csv").exists())
            self.assertFalse((root / "out/data/old.csv").exists())

    def test_counted_report(self):
        self.assertEqual(s.summarise_counts(StringIO(SAMPLE)),
                         ({"materials": {"cents": 1500, "count": 2},
                           "travel": {"cents": 300, "count": 1}}, [5]))
        self.assertEqual(s.summarise_counts(StringIO("category,cents\n")), ({}, []))
        self.assertEqual(s.summarise_counts(StringIO("category,cents\nx,0\n")),
                         ({"x": {"cents": 0, "count": 1}}, []))

    def test_counted_checkout(self):
        item = s.CountedLoanItem("Guide")
        item.checkout("Sam")
        with self.assertRaises(ValueError):
            item.checkout("Alex")
        self.assertEqual(item.checkout_count, 1)
        item.return_item()
        item.checkout("Alex")
        self.assertEqual(item.checkout_count, 2)

    def test_limit_and_count_views(self):
        with serving(handler_for(b'[{"topic":"x","minutes":25}]')) as url:
            self.assertEqual(len(s.fetch_with_daily_limit(url, 25)), 1)
            with self.assertRaises(ValueError):
                s.fetch_with_daily_limit(url, 24)
        records = [{"id": 1, "title": "<draft>", "done": False},
                   {"id": 2, "title": "x", "done": False},
                   {"id": 3, "title": "y", "done": True}]
        page = s.render_with_count(records)
        self.assertIn("Open requests: 2", page)
        self.assertIn("&lt;draft&gt;", page)
        self.assertIn("Open requests: 0", s.render_with_count([]))

    def test_due_date(self):
        self.assertEqual(s.parse_due_date("2026-12-01").isoformat(), "2026-12-01")
        for text in ("2026-02-30", "20261201", "tomorrow"):
            with self.subTest(text=text), self.assertRaises(ValueError):
                s.parse_due_date(text)
