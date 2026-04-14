from extensions.db import db
from datetime import datetime, timezone

class Todo(db.Model):
    __tablename__ = "todo"

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(255), nullable=False)

    # State fields
    in_progress = db.Column(db.Boolean, default=False)
    completed = db.Column(db.Boolean, default=False)

    # Who worked on it
    worked_by = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True)
    worked_by_user = db.relationship("User")

    # When it was completed
    completed_at = db.Column(db.DateTime, nullable=True)

    # Foreign key to Task
    task_id = db.Column(db.Integer, db.ForeignKey("task.id"), nullable=False)

    created_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc)
    )
    updated_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc)
    )

    # Relationship back to Task
    task = db.relationship("Task", back_populates="todos")
