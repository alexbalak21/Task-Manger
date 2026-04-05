# Task Manager

Task Manager is a Flask API for managing users and tasks. The application uses Flask, SQLAlchemy, JWT authentication, bcrypt password hashing, and a MySQL database.

## Overview

The main application entry point is [api/App.py](api/App.py). On startup it:

1. Loads configuration from [api/config/config.py](api/config/config.py).
2. Initializes the database, bcrypt, and JWT extensions.
3. Registers the auth, user, and task blueprints.
4. Exposes a health check at `/` and API docs at `/api/docs`.
5. Creates tables and seeds initial data when the database is available.

If automatic database initialization fails, you can run the Flask CLI command `flask init-db` from the `api` directory.

## Requirements

- Python 3.14 or compatible
- MySQL
- The packages listed in [api/req.txt](api/req.txt)

## Configuration

The app reads these environment variables:

- `MYSQL_HOST`
- `MYSQL_PORT`
- `MYSQL_USER`
- `MYSQL_PASSWORD`
- `MYSQL_DB`
- `SECRET_KEY`
- `JWT_SECRET_KEY`
- `CORS_ALLOWED_ORIGINS`

The repository includes [api/.flaskenv](api/.flaskenv) with local defaults for MySQL and Flask debug mode.

## Run the API

From the `api` folder:

```powershell
python -m venv env
.\env\Scripts\Activate.ps1
pip install -r req.txt
flask --app App run --debug
```

If the database is already reachable, the app will create the schema and seed base data on startup.

To initialize manually:

```powershell
flask --app App init-db
```

## API Endpoints

### Health

- `GET /` - returns `{"status": "Server is running"}`
- `GET /api/docs` - serves the API markdown documentation

### Auth

- `POST /api/auth/register` - register a new user
- `POST /api/auth/login` - log in and receive tokens
- `POST /api/auth/refresh` - exchange a refresh token for new tokens
- `POST /api/auth/logout` - logout protected by JWT

### User

- `GET /api/user` - get the current authenticated user
- `PUT /api/user` - update the current authenticated user
- `POST /api/user/password` - change the current user's password

### Tasks

- `GET /api/tasks` - list tasks for authenticated users
- `GET /api/tasks/<task_id>` - get a task by id
- `POST /api/tasks` - create a task, admin only
- `PUT /api/tasks/<task_id>` - update a task
- `DELETE /api/tasks/<task_id>` - delete a task, admin only

## Notes

- Task create and delete actions require an admin user.
- Authentication uses JWT access and refresh tokens.
- Seed data is loaded from the files in [api/seed](api/seed).
