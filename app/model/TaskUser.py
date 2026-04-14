from extensions.db import db

# Association table for many-to-many between User and Task
users_tasks = db.Table(
    "users_tasks",
    db.Column("user_id", db.Integer, db.ForeignKey("user.id"), primary_key=True),
    db.Column("task_id", db.Integer, db.ForeignKey("task.id"), primary_key=True)
)
