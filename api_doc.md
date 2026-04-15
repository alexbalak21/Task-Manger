# Task Manager API Documentation

## Overview

Task Manager is a Flask-based REST API for managing users and tasks. It uses SQLAlchemy for ORM, JWT for authentication, and supports user profile images. The API is organized into controllers, models, and services.

---

## App Structure
- **Entrypoint:** `App.py`
- **Blueprints:**
  - `/api/auth` (AuthController)
  - `/api/user` (UserController)
  - `/api/tasks` (TaskController)
  - `/api/todos` (TodoController)
- **Other routes:**
  - `/` (health check)
  - `/api/docs` (serves this documentation)

---

## Authentication
- JWT access and refresh tokens
- Passwords hashed with bcrypt
- Admin-only actions enforced via custom decorator

---

## Models

### User
- `id`: int, primary key
- `name`: string, required
- `email`: string, unique, required
- `password_hash`: string, required
- `role`: string, default 'user'
- `created_at`, `updated_at`: datetime
- Methods: `set_password`, `check_password`

### Task
- `id`: int, primary key
- `title`: string, required
- `description`: text, optional
- `priority_id`: int, FK to Priority
- `status_id`: int, FK to Status
- `start_date`, `due_date`: datetime, optional
- `created_at`, `updated_at`: datetime
- `users`: many-to-many with User

### Priority
- `id`: int, primary key
- `name`: string, unique, required

### Status
- `id`: int, primary key
- `name`: string, unique, required

### Comment
- `id`: int, primary key
- `content`: text, required
- `user_id`: int, FK to User
- `task_id`: int, FK to Task
- `created_at`: datetime

### Todo
- `id`: int, primary key
- `text`: string, required
- `in_progress`: bool
- `completed`: bool
- `worked_by`: int, FK to User
- `completed_at`: datetime
- `task_id`: int, FK to Task
- `created_at`, `updated_at`: datetime

### Attachments
- `id`: int, primary key
- `text`: text, required
- `created_by`: int, FK to User
- `created_at`: datetime

### UserProfileImage
- `user_id`: int, FK to User, primary key
- `blob`: binary (image data)

---

## Controllers & Routes

### AuthController (`/api/auth`)
- `POST /register`: Register new user, returns tokens and user
- `POST /login`: Authenticate, returns tokens and user
- `POST /refresh`: Refresh tokens
- `POST /logout`: Logout (JWT required)

### UserController (`/api/user`)
- `GET /`: Get current user info (JWT required)
- `PUT /`: Update user info (JWT required)
- `POST /password`: Change password (JWT required)
- `POST /register`: Register user (alternative to AuthController)

### TaskController (`/api/tasks`)
- `GET /`: List all tasks (JWT required)
- `GET /<task_id>`: Get task by ID (JWT required)
- `POST /`: Create task (admin only)
- `PUT /<task_id>`: Update task (JWT required)
- `DELETE /<task_id>`: Delete task (admin only)

### TodoController (`/api/todos`)
- `GET /`: List all todos (JWT required)
- `GET /task/<task_id>`: List todos for a task (JWT required)
- `GET /<todo_id>`: Get todo by ID (JWT required)
- `POST /`: Create todo (JWT required)
- `PUT /<todo_id>`: Update todo (JWT required)
- `DELETE /<todo_id>`: Delete todo (admin only)

---

## Services

### AuthService
- `register(name, email, password, profile_image=None)`: Register user, process image, return tokens
- `login(email, password)`: Authenticate, return tokens

### UserService
- `get_user(user_id)`: Return user DTO
- `update_user(user_id, data)`: Update user fields
- `change_password(user, current, new)`: Change password
- `register_user(data, profile_image=None)`: Register user (alternative)

### TaskService
- `get_all()`: List all tasks
- `get_by_id(task_id)`: Get task by ID
- `create(data)`: Create task (validates fields)
- `update(task, data)`: Update task fields
- `delete(task)`: Delete task

### TodoService
- `get_all()`: List all todos
- `get_by_id(todo_id)`: Get todo by ID
- `get_by_task_id(task_id)`: List todos for a task
- `create(data)`: Create todo (validates fields)
- `update(todo, data)`: Update todo fields
- `delete(todo)`: Delete todo

### ProfileImageService
- `process_profile_image(file_storage)`: Validate, resize, and encode image
- `save_for_user(user_id, image_bytes)`: Save or update profile image

---

## DTO Shapes

### User DTO
- Fields: id, name, email, role, created_at, updated_at, etc.

### Task DTO
- Fields: id, title, description, priority_id, status_id, start_date, due_date, created_at, updated_at

### Todo DTO
- Fields: id, text, in_progress, completed, worked_by, completed_at, task_id, created_at, updated_at

---

## Status & Priority
- Statuses: Pending, Awaiting, Scheduled, In Progress, On Hold, Blocked, Completed, Cancelled
- Priorities: Low, Medium, High

---

## Error Handling
- 404: JSON error for API routes, React index.html for frontend
- 500: JSON error for API routes
- JWT errors: Custom JSON responses for expired, invalid, missing, or revoked tokens

---

## Security
- JWT required for most routes
- Admin-only actions for task creation/deletion
- Passwords hashed with bcrypt

---

## Example Requests

### Register
```
POST /api/auth/register
{
  "name": "John Doe",
  "email": "john@example.com",
  "password": "password123"
}
```

### Login
```
POST /api/auth/login
{
  "email": "john@example.com",
  "password": "password123"
}
```

### Create Task (admin)
```
POST /api/tasks
Authorization: Bearer <admin_token>
{
  "title": "New Task",
  "priority_id": 1,
  "status_id": 1
}
```

### Create Todo
```
POST /api/todos
Authorization: Bearer <user_token>
{
  "text": "Subtask 1",
  "task_id": 1
}
```

### Get Todos for a Task
```
GET /api/todos/task/1
Authorization: Bearer <user_token>
```

### Update Todo
```
PUT /api/todos/5
Authorization: Bearer <user_token>
{
  "completed": true
}
```

### Delete Todo (admin)
```
DELETE /api/todos/5
Authorization: Bearer <admin_token>
```

---

## Notes
- Task creation and deletion require admin privileges
- All date fields use ISO 8601 format
- Profile images are stored as JPEG, max 2MB, 100x100px

---

## Health Check
- `GET /` returns `{ "status": "Server is running" }`

---

## API Docs
- `GET /api/docs` returns this file as markdown
