from pathlib import Path
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]


class ChapterOneTests(unittest.TestCase):
    def run_example(self, name):
        result = subprocess.run(
            [sys.executable, str(ROOT / "examples/ch01" / name)],
            cwd=ROOT, capture_output=True, text=True, timeout=10, check=True,
        )
        self.assertEqual(result.stderr, "")
        return result.stdout

    def test_practice_output(self):
        self.assertEqual(self.run_example("practice.py"),
                         "Today's practice\nReading minutes: 10\nTotal minutes: 15\n")

    def test_exercise_solution(self):
        self.assertEqual(self.run_example("my_practice.py"),
                         "Learning to organise my files\nReading minutes: 12\nTotal minutes: 19\n")

    def test_deliberately_missing_parenthesis(self):
        with self.assertRaises(SyntaxError):
            compile('print("Ready to practise"', "scratch.py", "exec")
