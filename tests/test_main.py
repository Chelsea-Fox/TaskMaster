from unittest import TestCase
from src.main import get_task


class Test(TestCase):
    def test_input_is_passed_and_returned(self):
        expected_value = "Clean"
        actual_value = get_task("Clean")

        self.assertEqual(expected_value, actual_value, "Values are not matching")
