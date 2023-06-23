"""Flask app for task_master"""
import json
import logging
from datetime import datetime
from functools import wraps

from flask import Flask, request, make_response, Response
from flask_basicauth import BasicAuth
from tasks import Tasks, InvalidTaskError, SchemaMissingKeyError

app = Flask(__name__)

app.config["BASIC_AUTH_USERNAME"] = "task_master"
app.config["BASIC_AUTH_PASSWORD"] = "MasterOfTasks"

basic_auth = BasicAuth(app)

tasks = Tasks()

# Configure logging
logging.basicConfig(level=logging.DEBUG)


def format_response(func):
    """Decorator to format response to json"""

    @wraps(func)
    def decorated_function(*args, **kwargs):
        # Invoke the original route function
        try:
            response = func(*args, **kwargs)
        except (InvalidTaskError, SchemaMissingKeyError) as invalid_data:
            logging.info(invalid_data)
            return Response(str(invalid_data), status=400)
        except Exception as server_error:  # pylint: disable=broad-exception-caught
            logging.error(server_error)
            return Response("Internal Server Error", status=500)

        # Convert the response to JSON
        json_response = json.dumps(response)

        # Create a Flask response with JSON content type
        flask_response = make_response(json_response)
        flask_response.headers["Content-Type"] = "application/json"

        logging.debug("Response = %s", json_response)

        return flask_response

    return decorated_function


@app.route("/tasks")
@basic_auth.required
@format_response
def tasks_get():
    """Route /tasks"""
    response = tasks.get_tasks()
    for task in response:
        convert_datetime_to_iso(task)

    return response


@app.route("/tasks/due")
@basic_auth.required
@format_response
def get_tasks_due():
    """Route /tasks/due"""

    due_date = None

    if "duedate" in request.args:
        due_date = datetime.strptime(request.args.get("duedate"), "%Y-%m-%dT%H:%M:%S")

    response = tasks.get_due_tasks(due_date)
    for task in response:
        convert_datetime_to_iso(task)

    return response


@app.route("/task", methods=["POST"])
@basic_auth.required
@format_response
def tasks_post():
    """Route for POST /task"""
    task = request.get_json()

    logging.debug("Request body for POST task = %s", task)

    task["eta"] = datetime.strptime(task["eta"], "%Y-%m-%dT%H:%M:%S")

    saved_task = tasks.post_task(task)

    convert_datetime_to_iso(saved_task)

    return saved_task


@app.route("/task/<task_id>")
@basic_auth.required
@format_response
def get_task(task_id):
    """Route for GET /task>"""
    response = tasks.get_tasks(task_id)

    convert_datetime_to_iso(response[0])

    return response


@app.route("/task/<task_id>", methods=["DELETE"])
@basic_auth.required
def delete_task(task_id):
    """Route for DELETE task"""
    tasks.delete_task(task_id)

    return "", 204


@app.route("/task/<task_id>", methods=["PUT"])
@basic_auth.required
@format_response
def put_task(task_id):
    """Route for PUT task"""

    task = request.get_json()

    logging.debug("Request body for PUT task = %s", task)

    task["eta"] = datetime.strptime(task["eta"], "%Y-%m-%dT%H:%M:%S")

    updated_task = tasks.put_task(task_id, task)
    convert_datetime_to_iso(updated_task)

    return updated_task


@app.route("/task/<task_id>/complete", methods=["PATCH"])
@basic_auth.required
@format_response
def complete_task(task_id):
    """Route for complete task"""

    task = tasks.complete_task(task_id)
    convert_datetime_to_iso(task)

    return task


def convert_datetime_to_iso(response):
    """datetime to ISO string conversion"""
    response["eta"] = response["eta"].isoformat()


if __name__ == "__main__":
    app.run(debug=True)
