from model.Task import Task
from extensions.db import db

class TaskRepository:
	@staticmethod
	def get_all():
		return Task.query.all()

	@staticmethod
	def get_by_id(task_id):
		return Task.query.get(task_id)

	@staticmethod
	def create(task):
		db.session.add(task)
		db.session.commit()
		return task

	@staticmethod
	def update():
		db.session.commit()

	@staticmethod
	def delete(task):
		db.session.delete(task)
		db.session.commit()
