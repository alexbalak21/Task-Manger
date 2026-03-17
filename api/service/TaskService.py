from repository.TaskRepository import TaskRepository
from model.Task import Task
from model.Priority import Priority
from model.Status import Status

class TaskService:
	@staticmethod
	def get_all():
		return TaskRepository.get_all()

	@staticmethod
	def get_by_id(task_id):
		return TaskRepository.get_by_id(task_id)

	@staticmethod
	def create(data):
		task = Task(
			title=data["title"],
			description=data.get("description"),
			priority_id=data["priority_id"],
			status_id=data["status_id"],
			due_date=data.get("due_date")
		)
		return TaskRepository.create(task)

	@staticmethod
	def update(task, data):
		if "title" in data:
			task.title = data["title"]
		if "description" in data:
			task.description = data["description"]
		if "priority_id" in data:
			task.priority_id = data["priority_id"]
		if "status_id" in data:
			task.status_id = data["status_id"]
		if "due_date" in data:
			task.due_date = data["due_date"]
		TaskRepository.update(task)
		return task

	@staticmethod
	def delete(task):
		TaskRepository.delete(task)
