from datetime import datetime, timezone

from extensions.db import db


class Attachment(db.Model):
	__tablename__ = "attachment"

	id = db.Column(db.Integer, primary_key=True)
	text = db.Column(db.Text, nullable=False)

	created_by = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
	user = db.relationship("User")

	created_at = db.Column(
		db.DateTime,
		default=lambda: datetime.now(timezone.utc)
	)
