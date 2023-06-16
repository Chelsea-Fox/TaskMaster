"""
Main file for TaskMaster
"""
from datetime import datetime
from enum import Enum
import pickle
from schema import Schema
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
