"""
tasks functionality
"""
import copy
import logging
import uuid
from datetime import datetime
from enum import Enum
import pickle
from functools import wraps

from schema import Schema, SchemaMissingKeyError, SchemaWrongKeyError, Optional, Use
import settings


# Configure logging
logging.basicConfig(level=logging.DEBUG)


def deep_copy_params_method(func):
    """Decorator to copy input and output parameters"""

    @wraps(func)
    def decorated_method(self, *args, **kwargs):
        # Create deep copies of input parameters
        copied_args = copy.deepcopy(args)
        copied_kwargs = copy.deepcopy(kwargs)

        # Invoke the original function with copied parameters
        result = func(self, *copied_args, **copied_kwargs)

        # Create a deep copy of the result
        copied_result = copy.deepcopy(result)

        # Return the deep copied result
        return copied_result

    return decorated_method


class Status(Enum):
    """Enum for Statuses"""

    OPEN = "OPEN"
    DONE = "DONE"
    CANCELLED = "CANCELLED"


def validate_task(task):
    """
    Accepts and validates a task.
    :param task: dict: The task to be accepted.
    :return: Task being passed
    """
    schema = Schema(
        {"description": str, "eta": datetime, "status": str, Optional("_id"): Use(str)}
    )
    schema.validate(task)
    Status(task["status"])

    return task


# pylint: disable=too-few-public-methods
class InvalidTaskError(Exception):
    """Exception for invalid task."""


class Tasks:
    """Class for tasks management."""

    def __init__(self):
        self._task_list = {}
        self.load_tasks()

    @deep_copy_params_method
    def post_task(self, task):
        """
        Posts a given task to the task list
        :param task:
        :return: dict: task with '_id' assigned
        """
        try:
            validate_task(task)
        except (SchemaMissingKeyError, SchemaWrongKeyError) as schema_key_error:
            logging.info(
                "error on post_task, invalid task received -- %s", schema_key_error
            )
            raise InvalidTaskError(schema_key_error) from schema_key_error
        except ValueError as wrong_status:
            logging.info(
                "error on post_task, invalid task status received -- %s", wrong_status
            )
            raise InvalidTaskError(wrong_status) from wrong_status

        uid = str(uuid.uuid4())
        task["_id"] = uid
        self._task_list[uid] = task

        self.save_tasks()

        return task

    @deep_copy_params_method
    def get_tasks(self, task_id=None):
        """
        Gets a list of tasks that match filter criteria, returning all if criteria is None.
        :return: list: tasks
        """
        if task_id is None:
            return list(self._task_list.values())

        return [x for x in [self._task_list.get(task_id)] if x is not None]

    @deep_copy_params_method
    def get_due_tasks(self, due_date=None):
        """
        Gets a list of tasks that are due to be completed.
        :param: due_date: Datetime.datetime: Due date for tasks, defaults to today
        :return: list: tasks matching criteria
        """
        if due_date is None:
            due_date = datetime.now()

        return [x for x in self._task_list.values() if x["eta"] <= due_date]

    def delete_task(self, task_id):
        """
        Deletes a task given its task_id
        :param task_id: id given to delete a task
        :return: None
        """
        self._task_list.pop(task_id, None)
        self.save_tasks()

    @deep_copy_params_method
    def put_task(self, task_id, updated_task):
        """
        Updates a task given its task_id and updated_task
        :param task_id: id given to update a task
        :param updated_task: dict: updated task
        :return: None
        """
        try:
            validate_task(updated_task)
        except (SchemaMissingKeyError, SchemaWrongKeyError) as schema_key_error:
            logging.info(
                "error on post_task, invalid task received -- %s", schema_key_error
            )
            raise InvalidTaskError(schema_key_error) from schema_key_error
        except ValueError as wrong_status:
            logging.info(
                "error on post_task, invalid task status received -- %s", wrong_status
            )
            raise InvalidTaskError(wrong_status) from wrong_status

        self._task_list[task_id] = updated_task

        self.save_tasks()

        return updated_task

    @deep_copy_params_method
    def complete_task(self, task_id):
        """
        Updates task status to DONE given task id
        :param task_id: id given to update a task
        :return: dict: updated task
        """
        self._task_list[task_id]["status"] = "DONE"
        self.save_tasks()

        return self._task_list[task_id]

    def save_tasks(self):
        """
        Saves tasks
        :return: None
        """
        with open(settings.TASK_DATA_FILE, "wb") as file:
            pickle.dump(self._task_list, file)

    def load_tasks(self):
        """
        Loads tasks
        :return: None
        """

        tasks = {}
        try:
            with open(settings.TASK_DATA_FILE, "rb") as file:
                tasks = pickle.load(file)
        except FileNotFoundError:
            with open(settings.TASK_DATA_FILE, "wb") as file:
                pickle.dump(tasks, file)

        self._task_list = tasks
