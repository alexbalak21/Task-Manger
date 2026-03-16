from extensions.db import db
from datetime import datetime, timezone
from model.TaskUser import users_tasks
from model.Priority import Priority
from model.Status import Status


class Task(db.Model):
    __tablename__ = "task"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)

    # Priority FK
    priority_id = db.Column(db.Integer, db.ForeignKey("priority.id"), nullable=False)
    priority_obj = db.relationship("Priority", back_populates="tasks")
    
    # Status FK
    status_id = db.Column(db.Integer, db.ForeignKey("status.id"), nullable=False)
    status_obj = db.relationship("Status", back_populates="tasks")

    due_date = db.Column(db.DateTime, nullable=True)

    # Timezone-aware timestamps
    created_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc)
    )
    updated_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc)
    )

    # Many-to-many users
    users = db.relationship(
        "User",
        secondary=users_tasks,
        backref="tasks"
    )
