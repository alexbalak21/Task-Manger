from model.Task import Task
from extensions.db import db
from sqlalchemy import func
from model.Todo import Todo

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



	@staticmethod
	def get_all_with_stats():
		return (
			db.session.query(
				Task,
				func.count(Todo.id).label("total_todos"),
				func.sum(func.if_(Todo.completed == True, 1, 0)).label("completed_todos")
			)
			.outerjoin(Todo, Todo.task_id == Task.id)
			.group_by(Task.id)
			.all()
		)