# Todo API Documentation

This document describes the API endpoints for managing todos in the application. All endpoints require JWT authentication unless otherwise specified.

---

## GET /api/todos
**Description:** Get all todos.
- **Auth:** JWT required
- **Response:** 200 OK, list of todos

---

## GET /api/todos/task/<task_id>
**Description:** Get all todos for a specific task.
- **Auth:** JWT required
- **Params:**
  - `task_id` (int): Task ID
- **Response:** 200 OK, list of todos

---

## GET /api/todo/ids
**Description:** Get todos by a list of IDs (from JSON body).
- **Auth:** JWT required
- **Body:**
  - `todos_ids` (list of int): List of todo IDs
- **Response:** 200 OK, list of todos
- **Errors:** 400 if `todos_ids` is not a list or contains non-integers

---

## GET /api/todos/<todo_id>
**Description:** Get a single todo by ID.
- **Auth:** JWT required
- **Params:**
  - `todo_id` (int): Todo ID
- **Response:** 200 OK, todo object
- **Errors:** 404 if not found

---

## POST /api/todos
**Description:** Create a new todo.
- **Auth:** Admin only
- **Body:** JSON with todo fields
- **Response:** 201 Created, todo object
- **Errors:** 400 if validation fails

---

## PUT /api/todos/<todo_id>
**Description:** Update a todo.
- **Auth:** JWT required
- **Params:**
  - `todo_id` (int): Todo ID
- **Body:** JSON with fields to update
- **Response:** 200 OK, updated todo object
- **Errors:** 404 if not found, 400 if validation fails

---

## DELETE /api/todos/<todo_id>
**Description:** Delete a todo.
- **Auth:** Admin only
- **Params:**
  - `todo_id` (int): Todo ID
- **Response:** 200 OK, message
- **Errors:** 404 if not found

---

## Todo Object Example
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
