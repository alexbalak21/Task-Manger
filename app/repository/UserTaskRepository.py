from extensions.db import db
from model.UserTask import users_tasks

class UserTaskRepository:
    @staticmethod
    def assign_user_to_task(user_id, task_id):
        ins = users_tasks.insert().values(user_id=user_id, task_id=task_id)
        db.session.execute(ins)
        db.session.commit()

    @staticmethod
    def unassign_user_from_task(user_id, task_id):
        delete = users_tasks.delete().where(
            (users_tasks.c.user_id == user_id) & (users_tasks.c.task_id == task_id)
        )
        db.session.execute(delete)
        db.session.commit()

    @staticmethod
    def get_users_for_task(task_id):
        result = db.session.execute(
            users_tasks.select().where(users_tasks.c.task_id == task_id)
        )
        return [row.user_id for row in result]

    @staticmethod
    def get_tasks_for_user(user_id):
        result = db.session.execute(
            users_tasks.select().where(users_tasks.c.user_id == user_id)
        )
        return [row.task_id for row in result]
