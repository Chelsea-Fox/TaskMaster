"""Flask app for task_master"""
import json
from datetime import datetime
from functools import wraps

from flask import Flask, request, make_response
from tasks import Tasks

app = Flask(__name__)
tasks = Tasks()


def format_response(func):
    """Decorator to format response to json"""

    @wraps(func)
    def decorated_function(*args, **kwargs):
        # Invoke the original route function
        response = func(*args, **kwargs)

        # Convert the response to JSON
        json_response = json.dumps(response)

        # Create a Flask response with JSON content type
        flask_response = make_response(json_response)
        flask_response.headers["Content-Type"] = "application/json"

        return flask_response

    return decorated_function


@app.route("/tasks")
@format_response
def tasks_get():
    """Route /tasks"""
    response = tasks.get_tasks()
    for task in response:
        convert_datetime_to_iso(task)

    return response


@app.route("/task", methods=["POST"])
@format_response
def tasks_post():
    """Route for POST /task"""
    task = request.get_json()
    task["eta"] = datetime.strptime(task["eta"], "%Y-%m-%dT%H:%M:%S")

    saved_task = tasks.post_task(task)

    convert_datetime_to_iso(saved_task)

    return saved_task


@app.route("/task/<task_id>")
@format_response
def get_task(task_id):
    """Route for GET /task>"""
    response = tasks.get_tasks(task_id)

    convert_datetime_to_iso(response[0])

    return response


@app.route("/task/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    """Route for DELETE task"""
    tasks.delete_task(task_id)

    return "", 204


@app.route("/task/<task_id>", methods=["PUT"])
@format_response
def put_task(task_id):
    "Route for PUT task"

    task = request.get_json()
    task["eta"] = datetime.strptime(task["eta"], "%Y-%m-%dT%H:%M:%S")

    updated_task = tasks.put_task(task_id, task)
    print(updated_task)
    convert_datetime_to_iso(updated_task)

    return updated_task


def convert_datetime_to_iso(response):
    """datetime to ISO string conversion"""
    response["eta"] = response["eta"].isoformat()


if __name__ == "__main__":
    app.run(debug=True)
