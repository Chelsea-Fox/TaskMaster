"""
Main test file for TaskMaster
"""
from unittest import TestCase
from main import get_task
from datetime import datetime, timedelta


# pylint: disable=missing-class-docstring
class Test(TestCase):
    clean_task = {
            "description": "Clean House",
            "eta": datetime.now() + timedelta(days=3),
            "status": "OPEN"
        }

    def test_input_is_passed_and_returned(self):
        """Simple input and output"""
        expected_value = self.clean_task
        actual_value = get_task(self.clean_task)

        self.assertEqual(expected_value, actual_value, "Values are not matching")

    def test_valid_task_is_accepted(self):
        return_value = get_task(self.clean_task)

        assert return_value is not None
