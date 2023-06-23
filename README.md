<img align="right" height="25px" src="https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue" />
<img align="right" height="25px" src="https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https%3A%2F%2Fgithub.com%2FChelsea-Fox%2Ftask_master%2F&count_bg=%2379C83D&title_bg=%23555555&icon=github.svg&icon_color=%23E7E7E7&title=Hits&edge_flat=true"/>
<br />

# Task Master

Flask API to manage and track tasks.

## Requirements

Python 3.10

[requirements.txt](https://github.com/Chelsea-Fox/task_master/blob/master/requirements.txt)

## Routes

### `GET /tasks`
- Description: Retrieves a list of tasks.
- Response format: JSON.
- Example response:
```json
[
  {
    "_id": 1,
    "title": "Task 1",
    "eta": "2023-06-24T10:00:00Z",
    "status": "OPEN"
  },
  {
    "_id": 2,
    "title": "Task 2",
    "eta": "2023-06-25T14:30:00Z",
    "status": "OPEN"
  }
]
```

### `GET /task/<task_id>`
- Description: Retrieves task based on an id.
- Response format: JSON.
- Example response:
```json
[
  {
    "_id": 1,
    "title": "Task 1",
    "eta": "2023-06-24T10:00:00Z",
    "status": "OPEN"
  }
]
```

### `POST /task`
- Description: Creates a task.
- Response format: JSON.
- Example request:
```json
[
  {
    "title": "Task 1",
    "eta": "2023-06-24T10:00:00Z",
    "status": "OPEN"
  }
]
```
- Example response:
```json
[
  {
    "_id": 1,
    "title": "Task 1",
    "eta": "2023-06-24T10:00:00Z",
    "status": "OPEN"
  }
]
```

### `PUT /task/<task_id>`
- Description: Updates a task based on a task id.
- Response format: JSON.
- Example request:
```json
[
  {
    "_id": 1,
    "title": "Task 1",
    "eta": "2023-06-24T10:00:00Z",
    "status": "OPEN"
  }
]
```
- Example response:
```json
[
  {
    "_id": 1,
    "title": "Task 1",
    "eta": "2023-06-24T10:00:00Z",
    "status": "OPEN"
  }
]
```

### `PATCH /task/<task_id>/complete`
- Description: Completes a task based on an id, setting the status to `DONE`.
- Response format: JSON.
- Example response:
```json
[
  {
    "_id": 1,
    "title": "Task 1",
    "eta": "2023-06-24T10:00:00Z",
    "status": "DONE"
  }
]
```

### `DELETE /task/<task_id>`
- Description: Deletes a task based on an id.
- Response format: `No content`


## Repo Owners
|<img height="auto" width="100" src="https://avatars.githubusercontent.com/u/74470736" />|<img height="auto" width="100" src="https://avatars.githubusercontent.com/u/136701596" />|<img height="auto" width="100" src="https://avatars.githubusercontent.com/u/47180787" />|
|-|-|-|
|[@Chelsea-Fox](https://github.com/Chelsea-Fox)|[@kjhohura244](https://github.com/kjhohura244)|[@hjribeiro](https://github.com/hjribeiro)|
