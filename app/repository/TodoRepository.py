from model.Todo import Todo
from extensions.db import db

class TodoRepository:
    @staticmethod
    def get_all():
        return Todo.query.all()

    @staticmethod
    def get_by_id(todo_id):
        return Todo.query.get(todo_id)

    @staticmethod
    def get_by_task_id(task_id):
        return Todo.query.filter_by(task_id=task_id).all()

    @staticmethod
    def get_by_ids(todo_ids):
        return Todo.query.filter(Todo.id.in_(todo_ids)).all()

    @staticmethod
    def create(todo, commit=True):
        db.session.add(todo)
        if commit:
            db.session.commit()
        return todo

    @staticmethod
    def update(todo):
        db.session.commit()
        return todo

    @staticmethod
    def delete(todo):
        db.session.delete(todo)
        db.session.commit()
