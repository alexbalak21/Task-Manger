# API Routes Documentation

This document describes routes registered by the active Flask app in App.py.

## App Overview

- App entrypoint: App.py
- Registered blueprints:
  - /api/auth (AuthController)
  - /api/user (UserController)
  - /api/tasks (TaskController)
- Extra app-level routes:
  - GET /
  - GET /api/docs

Notes:
- A legacy app bootstrap exists in App_new.py using HomeController, but it is not used by App.py.
- JWT authentication is enforced with `@jwt_required()` on protected routes.
- Admin-only task actions use a custom `admin_required` decorator.

## Base Routes

### GET /
- Purpose: Health check
- Auth: Public
- Response: `{ "status": "Server is running" }`

### GET /api/docs
- Purpose: Serves markdown API documentation file from `api_doc.md`
- Auth: Public
- Response: Markdown file content (`text/markdown`)

## Auth Routes (/api/auth)

### POST /api/auth/register
- Purpose: Register new user and issue tokens
- Auth: Public
- Body:
  - `name` (string, required)
  - `email` (string, required)
  - `password` (string, required)
- Success:
  - `201 Created`
  - `{ access_token, refresh_token, user }`
- Error:
  - `400 Bad Request` when email already exists

### POST /api/auth/login
- Purpose: Authenticate user and issue tokens
- Auth: Public
- Body:
  - `email` (string, required)
  - `password` (string, required)
- Success:
  - `200 OK`
  - `{ access_token, refresh_token, user }`
- Error:
  - `401 Unauthorized` for invalid credentials

### POST /api/auth/refresh
- Purpose: Exchange refresh token for new access and refresh tokens
- Auth: Public (token passed in body)
- Body:
  - `refresh_token` (string, required)
- Success:
  - `200 OK`
  - `{ access_token, refresh_token }`
- Error:
  - `401 Unauthorized` when missing or invalid refresh token

### POST /api/auth/logout
- Purpose: Logout acknowledgement endpoint
- Auth: JWT required
- Body: none
- Success:
  - `200 OK`
  - `{ "message": "Successfully logged out" }`

## User Routes (/api/user)

### GET /api/user
- Purpose: Get current authenticated user profile
- Auth: JWT required
- Body: none
- Success:
  - `200 OK`
  - User DTO

### PUT /api/user
- Purpose: Update current user profile
- Auth: JWT required
- Body (any of):
  - `name` (string, optional)
  - `email` (string, optional)
- Success:
  - `200 OK`
  - Updated user DTO

### POST /api/user/password
- Purpose: Change current user password
- Auth: JWT required
- Body:
  - `currentPassword` (string, required)
  - `newPassword` (string, required)
- Success:
  - `200 OK`
  - `{ "success": true, "message": "Password updated" }`
- Error:
  - `400 Bad Request` when current password is incorrect

## Task Routes (/api/tasks)

### GET /api/tasks
- Purpose: List all tasks
- Auth: JWT required
- Body: none
- Success:
  - `200 OK`
  - Array of task DTO objects

### GET /api/tasks/<task_id>
- Purpose: Fetch a single task by ID
- Auth: JWT required
- Path params:
  - `task_id` (integer)
- Success:
  - `200 OK`
  - Task DTO
- Error:
  - `404 Not Found` when task does not exist

### POST /api/tasks
- Purpose: Create task
- Auth: JWT required + admin role
- Body:
  - `title` (string, required)
  - `description` (string, optional)
  - `priority_id` (integer, required)
  - `status_id` (integer, required)
  - `start_date` (ISO datetime string, optional)
  - `due_date` (ISO datetime string, optional)
- Success:
  - `201 Created`
  - Created task DTO
- Errors:
  - `400 Bad Request` when required fields are missing or IDs/due_date are invalid
  - `403 Forbidden` when user is not admin

### PUT /api/tasks/<task_id>
- Purpose: Update task
- Auth: JWT required
- Path params:
  - `task_id` (integer)
- Body (any updatable field):
  - `title` (string, optional)
  - `description` (string, optional)
  - `priority_id` (integer, optional)
  - `status_id` (integer, optional)
  - `start_date` (ISO datetime string, optional)
  - `due_date` (ISO datetime string, optional)
- Success:
  - `200 OK`
  - Updated task DTO
- Errors:
  - `404 Not Found` when task does not exist
  - `400 Bad Request` for invalid IDs or invalid due_date format

### DELETE /api/tasks/<task_id>
- Purpose: Delete task
- Auth: JWT required + admin role
- Path params:
  - `task_id` (integer)
- Success:
  - `200 OK`
  - `{ "message": "Task deleted" }`
- Errors:
  - `404 Not Found` when task does not exist
  - `403 Forbidden` when user is not admin

## DTO Shapes (Observed)

### User DTO
Likely includes fields from `user_to_dto(user)` such as user identity/profile fields.

### Task DTO
Returned by TaskController `task_to_dto(task)`:
- `id`
- `title`
- `description`
- `priority_id`
- `status_id`
- `start_date` (ISO string or null)
- `due_date` (ISO string or null)
- `created_at` (ISO string or null)
- `updated_at` (ISO string or null)

## Quick Auth Matrix

- Public:
  - POST /api/auth/register
  - POST /api/auth/login
  - POST /api/auth/refresh
  - GET /
  - GET /api/docs
- JWT required:
  - POST /api/auth/logout
  - GET /api/user
  - PUT /api/user
  - POST /api/user/password
  - GET /api/tasks
  - GET /api/tasks/<task_id>
  - PUT /api/tasks/<task_id>
- JWT + admin role:
  - POST /api/tasks
  - DELETE /api/tasks/<task_id>
