from repository.TaskRepository import TaskRepository
from model.Task import Task
from model.Priority import Priority
from model.Status import Status
from model.User import User
from model.Todo import Todo
from service.AttachmentService import AttachmentService
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
	def _parse_todo_entries(todos_data):
		if todos_data is None:
			return []
		if not isinstance(todos_data, list):
			raise ValueError("todos must be an array")

		normalized = []
		for item in todos_data:
			if isinstance(item, str):
				text = item.strip()
				if not text:
					raise ValueError("todos cannot contain empty text values")
				normalized.append(text)
			elif isinstance(item, bool) or not isinstance(item, int):
				raise ValueError("todos must contain strings or integer IDs")
			else:
				normalized.append(item)

		# Preserve order while removing exact duplicates.
		return list(dict.fromkeys(normalized))

	@staticmethod
	def _validate_task_dates(start_date, due_date):
		if start_date and due_date and due_date < start_date:
			raise ValueError("due_date cannot be earlier than start_date")

	@staticmethod
	def get_all():
		return TaskRepository.get_all()

	@staticmethod
	def get_by_id(task_id):
		return TaskRepository.get_by_id(task_id)

	@staticmethod
	def create(data, created_by=None):
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

		start_date = (
			TaskService._parse_datetime_field(data.get("start_date"), "start_date").date()
			if data.get("start_date") is not None
			else None
		)
		due_date = (
			TaskService._parse_datetime_field(data.get("due_date"), "due_date").date()
			if data.get("due_date") is not None
			else None
		)

		TaskService._validate_task_dates(start_date, due_date)

		task = Task(
			title=data["title"],
			description=data.get("description"),
			priority_id=data["priority_id"],
			status_id=data["status_id"],
			start_date=start_date,
			due_date=due_date
		)

		try:
			TaskRepository.create(task, commit=False)
			db.session.flush()

			if users:
				task.users = users

			todo_entries = TaskService._parse_todo_entries(data.get("todos"))
			todo_ids = [entry for entry in todo_entries if isinstance(entry, int)]
			todo_texts = [entry for entry in todo_entries if isinstance(entry, str)]

			if todo_ids:
				existing_todos = Todo.query.filter(Todo.id.in_(todo_ids)).all()
				todo_by_id = {todo.id: todo for todo in existing_todos}
				missing_todo_ids = [todo_id for todo_id in todo_ids if todo_id not in todo_by_id]
				if missing_todo_ids:
					raise ValueError(f"Invalid todo IDs: {missing_todo_ids}")

				for todo_id in todo_ids:
					todo_by_id[todo_id].task_id = task.id

			if todo_texts:
				for todo_text in todo_texts:
					todo = Todo(
						text=todo_text,
						task_id=task.id,
						in_progress=False,
						completed=False
					)
					db.session.add(todo)

			AttachmentService.attach_to_task(task, data.get("attachments"), created_by)

			db.session.commit()
			return task
		except Exception:
			db.session.rollback()
			raise

	@staticmethod
	def update(task, data):
		next_start_date = task.start_date
		next_due_date = task.due_date

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
			next_start_date = (
				TaskService._parse_datetime_field(data["start_date"], "start_date").date()
				if data["start_date"] is not None
				else None
			)
		if "due_date" in data:
			next_due_date = (
				TaskService._parse_datetime_field(data["due_date"], "due_date").date()
				if data["due_date"] is not None
				else None
			)

		TaskService._validate_task_dates(next_start_date, next_due_date)
		task.start_date = next_start_date
		task.due_date = next_due_date
		TaskRepository.update(task)
		return task

	@staticmethod
	def delete(task):
		TaskRepository.delete(task)


	@staticmethod
	def get_all_with_stats():
		return TaskRepository.get_all_with_stats()

