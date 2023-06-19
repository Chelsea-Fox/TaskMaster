"""
Main test file for TaskMaster
"""
import copy
import pickle
from datetime import datetime, timedelta
from unittest import TestCase
import pytest
from schema import SchemaMissingKeyError
from tasks import validate_task, save_task, load_task, Tasks, InvalidTaskError
import settings


# pylint: disable=missing-class-docstring
class TestValidateTask(TestCase):
    clean_task = {
        "description": "Clean House",
        "eta": datetime.now() + timedelta(days=3),
        "status": "OPEN",
    }

    def test_input_is_passed_and_returned(self):
        """Simple input and output"""
        expected_value = self.clean_task
        actual_value = validate_task(self.clean_task)

        self.assertEqual(expected_value, actual_value, "Values are not matching")

    def test_valid_task_is_accepted(self):
        """Validation of task schema"""
        return_value = validate_task(self.clean_task)

        assert return_value is not None

    def test_invalid_task_throws_exception(self):
        """Invalid of task"""
        invalid_task = {
            "descriptionzzzzzzzzzzzzzz": "Cooking",
            "eta": datetime.now() + timedelta(days=3),
            "status": "OPEN",
        }
        with pytest.raises(SchemaMissingKeyError):
            validate_task(invalid_task)

    def test_invalid_status(self):
        """Invalid task status"""
        invalid_status_task = {
            "description": "Cooking",
            "eta": datetime.now() + timedelta(days=3),
            "status": "BLUE",
        }
        with pytest.raises(ValueError):
            validate_task(invalid_status_task)


class TestTaskStorage(TestCase):
    """Test class for save task"""

    valid_task = {
        "description": "Shopping",
        "eta": datetime.now() + timedelta(days=3),
        "status": "OPEN",
    }

    def test_save_task(self):
        """Test saving task"""

        save_task(self.valid_task)

        with open(settings.TASK_DATA_FILE, "rb") as file:
            task = pickle.load(file)
        self.assertEqual(self.valid_task, task, "Tasks don't match")

    def test_load_task(self):
        """Test loading task"""

        save_task(self.valid_task)

        task = load_task()

        self.assertEqual(self.valid_task, task, "Tasks don't match")


class TestTaskManagement(TestCase):
    """Tests for task management"""

    tasks = Tasks()
    valid_task = {
        "description": "Shopping",
        "eta": datetime.now() + timedelta(days=3),
        "status": "OPEN",
    }

    def test_create_task(self):
        """Test creating task"""
        expected_task = copy.deepcopy(self.valid_task)

        return_task = self.tasks.post_task(self.valid_task)
        expected_task["_id"] = return_task["_id"]

        self.assertEqual(expected_task, return_task, "Tasks don't match")

    def test_post_task_with_invalid_task(self):
        """Testing with invalid task."""

        invalid_task = {
            "descriptionnnnnnnnn": "Shopping",
            "eta": datetime.now() + timedelta(days=5),
            "status": "OPEN",
        }

        with pytest.raises(InvalidTaskError):
            self.tasks.post_task(invalid_task)

    def test_post_task_with_invalid_task_status(self):
        """Testing with invalid task status."""

        invalid_task = {
            "description": "Shopping",
            "eta": datetime.now() + timedelta(days=5),
            "status": "DEFINATELYNOTASTATUS",
        }

        with pytest.raises(InvalidTaskError):
            self.tasks.post_task(invalid_task)

    def test_get_all_tasks(self):
        """Test GET all tasks from list of tasks"""

        self.tasks.post_task(self.valid_task)
        task_list = self.tasks.get_tasks()

        self.assertGreaterEqual(len(task_list), 1, "No tasks returned")

    def test_get_task_by_id(self):
        """Test GET task by id"""
        input_task = self.tasks.post_task(self.valid_task)
        return_task = self.tasks.get_tasks(input_task["_id"])

        self.assertEqual(
            [input_task], return_task, "Returned task is not the same as input task"
        )

    def test_get_task_with_wrong_id_returns_empty_list(self):
        """Test GET task with wrong id"""
        return_task = self.tasks.get_tasks("BLAHHH")

        self.assertListEqual(return_task, [], "Returned task is not empty list")
