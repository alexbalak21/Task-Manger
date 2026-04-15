from repository.TodoRepository import TodoRepository
from model.Todo import Todo
from model.User import User
from datetime import datetime

class TodoService:
	@staticmethod
	def get_all():
		return TodoRepository.get_all()

	@staticmethod
	def get_by_id(todo_id):
		return TodoRepository.get_by_id(todo_id)

	@staticmethod
	def get_by_task_id(task_id):
		return TodoRepository.get_by_task_id(task_id)

	@staticmethod
	def create(data):
		if not data:
			raise ValueError("Request body is required")
		if "text" not in data:
			raise ValueError("text is required")
		if "task_id" not in data:
			raise ValueError("task_id is required")

		todo = Todo(
			text=data["text"],
			in_progress=data.get("in_progress", False),
			completed=data.get("completed", False),
			worked_by=data.get("worked_by"),
			completed_at=TodoService._parse_datetime_field(data.get("completed_at"), "completed_at"),
			task_id=data["task_id"]
		)
		return TodoRepository.create(todo)

	@staticmethod
	def update(todo, data):
		if "text" in data:
			todo.text = data["text"]
		if "in_progress" in data:
			todo.in_progress = data["in_progress"]
		if "completed" in data:
			todo.completed = data["completed"]
		if "worked_by" in data:
			todo.worked_by = data["worked_by"]
		if "completed_at" in data:
			todo.completed_at = TodoService._parse_datetime_field(data["completed_at"], "completed_at")
		TodoRepository.update(todo)
		return todo

	@staticmethod
	def delete(todo):
		TodoRepository.delete(todo)

	@staticmethod
	def create_bulk(todos_data, task_id):
		"""
		Create multiple todos for a task.
		todos_data: list of strings (todo text)
		task_id: the task ID to associate todos with
		Returns: list of created Todo objects
		"""
		created_todos = []
		for text in todos_data:
			todo = Todo(
				text=text,
				task_id=task_id,
				in_progress=False,
				completed=False
			)
			TodoRepository.create(todo, commit=False)
			created_todos.append(todo)
		return created_todos

	@staticmethod
	def _parse_datetime_field(value, field_name):
		if value is None:
			return None
		if isinstance(value, datetime):
			return value
		if isinstance(value, str):
			try:
				return datetime.fromisoformat(value.replace("Z", "+00:00"))
			except ValueError:
				raise ValueError(f"{field_name} must be a valid ISO datetime string")
		raise ValueError(f"{field_name} must be an ISO datetime string")
