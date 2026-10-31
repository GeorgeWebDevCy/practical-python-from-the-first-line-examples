from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory
import unittest

from examples.hello import greeting

ROOT = Path(__file__).resolve().parents[1]


class GreetingTests(unittest.TestCase):
    def test_default_greeting(self):
        self.assertEqual(greeting(), "Hello, Python!")

    def test_named_greeting(self):
        self.assertEqual(greeting("  Reader  "), "Hello, Reader!")

    def test_module_command(self):
        result = subprocess.run(
            [sys.executable, "-m", "examples.hello"], cwd=ROOT,
            capture_output=True, text=True, timeout=10, check=True,
        )
        self.assertEqual(result.stdout, "Hello, Python!\n")
        self.assertEqual(result.stderr, "")

    def test_script_from_another_directory(self):
        with TemporaryDirectory() as folder:
            result = subprocess.run(
                [sys.executable, str(ROOT / "examples/hello.py")], cwd=folder,
                capture_output=True, text=True, timeout=10, check=True,
            )
        self.assertEqual(result.stdout, "Hello, Python!\n")
        self.assertEqual(result.stderr, "")


if __name__ == "__main__":
    unittest.main()
