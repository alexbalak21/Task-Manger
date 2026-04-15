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
	def create(task, commit=True):
		db.session.add(task)
		if commit:
			db.session.commit()
		return task

	@staticmethod
	def update(task):
		db.session.commit()

	@staticmethod
	def delete(task):
		db.session.delete(task)
		db.session.commit()
