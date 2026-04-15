from repository.TaskRepository import TaskRepository
from model.Task import Task
from model.Priority import Priority
from model.Status import Status
from model.User import User
from model.Todo import Todo
from extensions.db import db
from datetime import datetime

class TaskService:
	@staticmethod
	def _parse_id_list_field(value, field_name):
		if value is None:
			return []
		if not isinstance(value, list):
			raise ValueError(f"{field_name} must be an array of IDs")

		ids = []
		for item in value:
			if isinstance(item, bool) or not isinstance(item, int):
				raise ValueError(f"{field_name} must contain integer IDs")
			ids.append(item)

		# Preserve order while dropping duplicates.
		return list(dict.fromkeys(ids))

	@staticmethod
	def _parse_datetime_field(value, field_name):
		if value is None:
			return None
		if isinstance(value, datetime):
			return value
		if isinstance(value, str):
			date_value = value.replace("Z", "+00:00")
			try:
				return datetime.fromisoformat(date_value)
			except ValueError:
				raise ValueError(f"{field_name} must be a valid ISO datetime string")
		raise ValueError(f"{field_name} must be an ISO datetime string")

	@staticmethod
	def get_all():
		return TaskRepository.get_all()

	@staticmethod
	def get_by_id(task_id):
		return TaskRepository.get_by_id(task_id)

	@staticmethod
	def create(data):
		if not data:
			raise ValueError("Request body is required")
		if "title" not in data:
			raise ValueError("title is required")
		if "priority_id" not in data:
			raise ValueError("priority_id is required")
		if "status_id" not in data:
			raise ValueError("status_id is required")

		priority = Priority.query.get(data["priority_id"])
		if not priority:
			raise ValueError("Invalid priority_id")

		status = Status.query.get(data["status_id"])
		if not status:
			raise ValueError("Invalid status_id")

		user_ids = TaskService._parse_id_list_field(data.get("users"), "users")

		users = []
		if user_ids:
			users = User.query.filter(User.id.in_(user_ids)).all()
			found_user_ids = {u.id for u in users}
			missing_user_ids = [user_id for user_id in user_ids if user_id not in found_user_ids]
			if missing_user_ids:
				raise ValueError(f"Invalid user IDs: {missing_user_ids}")

		task = Task(
			title=data["title"],
			description=data.get("description"),
			priority_id=data["priority_id"],
			status_id=data["status_id"],
			start_date=TaskService._parse_datetime_field(data.get("start_date"), "start_date"),
			due_date=TaskService._parse_datetime_field(data.get("due_date"), "due_date")
		)

		try:
			TaskRepository.create(task, commit=False)
			db.session.flush()

			if users:
				task.users = users

			# Handle todos: can be array of IDs or array of strings (text)
			if "todos" in data and data["todos"]:
				todos_data = data["todos"]
				if not isinstance(todos_data, list):
					raise ValueError("todos must be an array")
				
				for todo_item in todos_data:
					if isinstance(todo_item, str):
						# Create new todo from string text
						todo = Todo(
							text=todo_item,
							task_id=task.id,
							in_progress=False,
							completed=False
						)
						db.session.add(todo)
					elif isinstance(todo_item, int):
						# Link existing todo by ID
						existing_todo = Todo.query.get(todo_item)
						if not existing_todo:
							raise ValueError(f"Invalid todo ID: {todo_item}")
						existing_todo.task_id = task.id
					else:
						raise ValueError("todos must contain strings or integer IDs")

			db.session.commit()
			return task
		except Exception:
			db.session.rollback()
			raise

	@staticmethod
	def update(task, data):
		if "title" in data:
			task.title = data["title"]
		if "description" in data:
			task.description = data["description"]
		if "priority_id" in data:
			priority = Priority.query.get(data["priority_id"])
			if not priority:
				raise ValueError("Invalid priority_id")
			task.priority_id = data["priority_id"]
		if "status_id" in data:
			status = Status.query.get(data["status_id"])
			if not status:
				raise ValueError("Invalid status_id")
			task.status_id = data["status_id"]
		if "start_date" in data:
			task.start_date = TaskService._parse_datetime_field(data["start_date"], "start_date")
		if "due_date" in data:
			task.due_date = TaskService._parse_datetime_field(data["due_date"], "due_date")
		TaskRepository.update(task)
		return task

	@staticmethod
	def delete(task):
		TaskRepository.delete(task)
