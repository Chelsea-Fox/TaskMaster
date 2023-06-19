"""
tasks functionality
"""
import copy
import uuid
from datetime import datetime
from enum import Enum
import pickle
from schema import Schema, SchemaMissingKeyError
import settings


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
    schema = Schema({"description": str, "eta": datetime, "status": str})
    schema.validate(task)
    Status(task["status"])

    return task


def save_task(task):
    """
    Saves tasks
    :param task: dict: The task to be saved
    :return: None
    """
    with open(settings.TASK_DATA_FILE, "wb") as file:
        pickle.dump(task, file)


def load_task():
    """
    Loads tasks
    :return: dict: task
    """
    with open(settings.TASK_DATA_FILE, "rb") as file:
        task = pickle.load(file)

    return task


# pylint: disable=too-few-public-methods


class InvalidTaskError(Exception):
    """Exception for invalid task."""


class Tasks:
    """Class for tasks management."""

    def __init__(self):
        self._task_list = {}

    def post_task(self, task):
        """
        Posts a given task to the task list
        :param task:
        :return: dict: task with '_id' assigned
        """
        try:
            validate_task(task)
        except SchemaMissingKeyError as missing_key:
            print(f"error on post_task, invalid task received -- {missing_key}")
            raise InvalidTaskError(missing_key) from missing_key
        except ValueError as wrong_status:
            print(f"error on post_task, invalid task status received -- {wrong_status}")
            raise InvalidTaskError(wrong_status) from wrong_status

        new_task = copy.deepcopy(task)

        uid = str(uuid.uuid4())
        new_task["_id"] = uid
        self._task_list[uid] = new_task

        return new_task

    def get_tasks(self, task_id=None):
        """
        Gets a list of tasks that match filter criteria, returning all if criteria is None.
        :return: list: tasks
        """
        if task_id is None:
            return list(self._task_list.values())

        return [x for x in [self._task_list.get(task_id)] if x is not None]

    def delete_task(self, task_id):
        """
        Deletes a task given its task_id
        :param task_id: id given to delete a task
        :return: None
        """
        self._task_list.pop(task_id, None)
