## Todo API Documentation

This document describes the todo API routes registered by `TodoController.py`.

All routes require JWT authentication unless stated otherwise.

## Base Routes

The controller registers two blueprints:

- `/api/todos` for todo collection and item routes
- `/api` for the query-based todo lookup route

## GET /api/todos
- Purpose: List all todos
- Auth: JWT required
- Body: none
- Success:
	- `200 OK`
	- Array of todo DTO objects

## GET /api/todos/task/<task_id>
- Purpose: List all todos for a task
- Auth: JWT required
- Path params:
	- `task_id` (integer)
- Body: none
- Success:
	- `200 OK`
	- Array of todo DTO objects

## GET /api/todo/id
- Purpose: Fetch todos by a list of IDs passed as repeated query parameters
- Auth: JWT required
- Query params:
	- `id` (integer, repeatable)
- Example:
	- `/api/todo/id?id=1&id=2&id=3`
- Success:
	- `200 OK`
	- Array of todo DTO objects in the same order as the requested IDs when found
- Errors:
	- `400 Bad Request` when any provided `id` value is not an integer

## GET /api/todos/<todo_id>
- Purpose: Fetch a single todo by ID
- Auth: JWT required
- Path params:
	- `todo_id` (integer)
- Success:
	- `200 OK`
	- Todo DTO object
- Errors:
	- `404 Not Found` when the todo does not exist

## POST /api/todos
- Purpose: Create a new todo
- Auth: JWT required + admin role
- Body:
	- `text` (string, required)
	- `task_id` (integer, required)
	- `in_progress` (boolean, optional, default `false`)
	- `completed` (boolean, optional, default `false`)
	- `worked_by` (integer, optional)
	- `completed_at` (ISO datetime string, optional)
- Success:
	- `201 Created`
	- Created todo DTO object
- Errors:
	- `400 Bad Request` when the request body is missing or required fields are missing
	- `403 Forbidden` when the user is not an admin

## PUT /api/todos/<todo_id>
- Purpose: Update a todo
- Auth: JWT required
- Path params:
	- `todo_id` (integer)
- Body (any updatable field):
	- `text` (string, optional)
	- `in_progress` (boolean, optional)
	- `completed` (boolean, optional)
	- `worked_by` (integer, optional)
	- `completed_at` (ISO datetime string, optional)
- Success:
	- `200 OK`
	- Updated todo DTO object
- Errors:
	- `404 Not Found` when the todo does not exist
	- `400 Bad Request` when `completed_at` is not a valid ISO datetime string

## PATCH /api/todos/<todo_id>
- Purpose: Partially update todo state
- Auth: JWT required
- Path params:
	- `todo_id` (integer)
- Body:
	- `in_progress` (boolean, optional)
	- `completed` (boolean, optional)
- Notes:
	- The controller rejects requests that do not include either `in_progress` or `completed`.
	- The endpoint delegates to the same update service as PUT, so it can also accept the other mutable fields if they are included.
- Success:
	- `200 OK`
	- Updated todo DTO object
- Errors:
	- `404 Not Found` when the todo does not exist
	- `400 Bad Request` when the request does not include `in_progress` or `completed`
	- `400 Bad Request` when `completed_at` is not a valid ISO datetime string


## PATCH /api/todos/<todo_id>/reopen
- Purpose: Reopen a completed todo (change from completed back to in_progress state)
- Auth: JWT required
- Path params:
	- `todo_id` (integer)
- Body: none
- Success:
	- `200 OK`
	- Updated todo DTO object with `in_progress: true`, `completed: false`, `completed_at: null`
- Errors:
	- `404 Not Found` when the todo does not exist
	- `400 Bad Request` when the todo is not completed



## DELETE /api/todos/<todo_id>
- Purpose: Delete a todo
- Auth: JWT required + admin role
- Path params:
	- `todo_id` (integer)
- Success:
	- `200 OK`
	- `{ "message": "Todo deleted" }`
- Errors:
	- `404 Not Found` when the todo does not exist
	- `403 Forbidden` when the user is not an admin

## Todo DTO Shape

The controller returns todos using `todo_to_dto(todo)` with this shape:

```json
{
	"id": 1,
	"text": "Sample todo",
	"in_progress": false,
	"completed": false,
	"worked_by": 2,
	"completed_at": null,
	"task_id": 5,
	"created_at": "2024-05-14T12:00:00",
	"updated_at": "2024-05-14T12:00:00"
}
```

## Quick Auth Matrix

- JWT required:
	- GET /api/todos
	- GET /api/todos/task/<task_id>
	- GET /api/todo/id
	- GET /api/todos/<todo_id>
	- PUT /api/todos/<todo_id>
	- PATCH /api/todos/<todo_id>
- JWT + admin role:
	- POST /api/todos
	- DELETE /api/todos/<todo_id>
