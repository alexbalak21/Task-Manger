from repository.TaskRepository import TaskRepository
from model.Task import Task
from model.Priority import Priority
from model.Status import Status
from datetime import datetime

class TaskService:
	@staticmethod
	def _parse_due_date(value):
		if value is None:
			return None
		if isinstance(value, datetime):
			return value
		if isinstance(value, str):
			date_value = value.replace("Z", "+00:00")
			try:
				return datetime.fromisoformat(date_value)
			except ValueError:
				raise ValueError("due_date must be a valid ISO datetime string")
		raise ValueError("due_date must be an ISO datetime string")

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

		task = Task(
			title=data["title"],
			description=data.get("description"),
			priority_id=data["priority_id"],
			status_id=data["status_id"],
			due_date=TaskService._parse_due_date(data.get("due_date"))
		)
		return TaskRepository.create(task)

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
		if "due_date" in data:
			task.due_date = TaskService._parse_due_date(data["due_date"])
		TaskRepository.update(task)
		return task

	@staticmethod
	def delete(task):
		TaskRepository.delete(task)
