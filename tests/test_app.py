"""Tests for Flask app"""
import unittest

from app import app


class RouteTests(unittest.TestCase):
    """Test class for Flask routes"""

    valid_task = {
        "description": "Clean House",
        "eta": "2023-06-20T14:00:00",
        "status": "OPEN",
    }

    def setUp(self):
        """Setup of application"""
        app.testing = True
        self.app = app.test_client()

    def get_tasks_with_empty_data(self):
        """testing get returns no data"""
        response = self.app.get("/tasks")
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data, [])

    def post_task_successful_and_get_task_by_id(self):
        """Test post route and get task by id"""
        response = self.app.post("/task", json=self.valid_task)
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        assert "_id" in data
        assert data["description"] == "Clean House"
        assert data["eta"] == "2023-06-20T14:00:00"
        assert data["status"] == "OPEN"
        assert response.headers.get("content-type") == "application/json"

        self.valid_task["_id"] = data["_id"]

        response = self.app.get(f"/task/{self.valid_task['_id']}")
        data = response.get_json()[0]

        self.assertEqual(response.status_code, 200)
        assert data["_id"] == self.valid_task["_id"]
        assert data["description"] == "Clean House"
        assert data["eta"] == "2023-06-20T14:00:00"
        assert data["status"] == "OPEN"
        assert response.headers.get("content-type") == "application/json"

    def get_tasks_should_return_data(self):
        """Test get tasks should return data"""
        response = self.app.get("/tasks")
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data), 1)
        data = data[0]
        assert data["_id"] == self.valid_task["_id"]
        assert data["description"] == "Clean House"
        assert data["eta"] == "2023-06-20T14:00:00"
        assert data["status"] == "OPEN"
        assert response.headers.get("content-type") == "application/json"

    def delete_task(self):
        """Step to delete task"""
        response = self.app.delete(f"/task/{self.valid_task['_id']}")

        self.assertEqual(response.status_code, 204)

    def test_get_and_post(self):
        """Test script for Flask API"""
        self.get_tasks_with_empty_data()
        self.post_task_successful_and_get_task_by_id()
        self.get_tasks_should_return_data()
        self.delete_task()
        self.get_tasks_with_empty_data()
