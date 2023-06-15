from unittest import TestCase
from src.main import get_task


class Test(TestCase):
    def test_get_input(self):
        get_task("Clean")
