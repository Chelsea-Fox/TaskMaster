"""
Main file for TaskMaster
"""
from datetime import datetime
from schema import Schema
from enum import Enum


class Status(Enum):
    OPEN = "OPEN"
    DONE = "DONE"
    CANCELLED = "CANCELLED"


def get_task(task):
    """
    Accepts a task and prints to console.
    :param task: str: The task to be accepted.
    :return: Task being passed
    """
    schema = Schema({'description': str,
                     'eta': datetime,
                     'status': str})

    Status(task["status"])

    schema.validate(task)

    return task
