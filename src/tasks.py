"""
tasks functionality
"""

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

        uid = str(uuid.uuid4())
        task["_id"] = uid
        self._task_list[uid] = task

        return self._task_list[uid]
