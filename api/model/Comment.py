from extensions.db import db
from datetime import datetime, timezone

class Comment(db.Model):
    __tablename__ = "comment"

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)

    # Who wrote the comment
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    user = db.relationship("User")

    # Which task it belongs to
    task_id = db.Column(db.Integer, db.ForeignKey("task.id"), nullable=False)

    created_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc)
    )
