"""
Main test file for TaskMaster
"""
from datetime import datetime, timedelta
from unittest import TestCase
import pytest
from schema import SchemaMissingKeyError
from main import get_task


# pylint: disable=missing-class-docstring
class Test(TestCase):
    clean_task = {
        "description": "Clean House",
        "eta": datetime.now() + timedelta(days=3),
        "status": "OPEN",
    }

    def test_input_is_passed_and_returned(self):
        """Simple input and output"""
        expected_value = self.clean_task
        actual_value = get_task(self.clean_task)

        self.assertEqual(expected_value, actual_value, "Values are not matching")

    def test_valid_task_is_accepted(self):
        """Validation of task schema"""
        return_value = get_task(self.clean_task)

        assert return_value is not None

    def test_invalid_task_throws_exception(self):
        """Invalid of task"""
        invalid_task = {
            "descriptionzzzzzzzzzzzzzz": "Cooking",
            "eta": datetime.now() + timedelta(days=3),
            "status": "OPEN",
        }
        with pytest.raises(SchemaMissingKeyError):
            get_task(invalid_task)

    def test_invalid_status(self):
        """Invalid task status"""
        invalid_status_task = {
            "description": "Cooking",
            "eta": datetime.now() + timedelta(days=3),
            "status": "BLUE",
        }
        with pytest.raises(ValueError):
            get_task(invalid_status_task)
