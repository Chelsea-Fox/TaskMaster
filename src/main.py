"""
Main file for TaskMaster
"""
from datetime import datetime
from enum import Enum
from schema import Schema


class Status(Enum):
    """Enum for Statuses"""

    OPEN = "OPEN"
    DONE = "DONE"
    CANCELLED = "CANCELLED"


def get_task(task):
    """
    Accepts and validates a task.
    :param task: str: The task to be accepted.
    :return: Task being passed
    """
    schema = Schema({"description": str, "eta": datetime, "status": str})
    schema.validate(task)
    Status(task["status"])

    return task
