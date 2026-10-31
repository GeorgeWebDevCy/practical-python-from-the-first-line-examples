import unittest

from examples.ch08.durations import parse_minutes


class DurationContractTests(unittest.TestCase):
    def test_valid_values(self):
        self.assertEqual(parse_minutes(" 25 "), 25)
        self.assertEqual(parse_minutes("0"), 0)

    def test_invalid_values(self):
        for text in ["-2", "many", "2.5"]:
            with self.subTest(text=text):
                with self.assertRaises(ValueError):
                    parse_minutes(text)


if __name__ == "__main__":
    unittest.main()
