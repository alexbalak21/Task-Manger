from extensions.db import db


# Association table for many-to-many between Task and Attachment
task_attachments = db.Table(
	"task_attachments",
	db.Column("task_id", db.Integer, db.ForeignKey("task.id"), primary_key=True),
	db.Column("attachment_id", db.Integer, db.ForeignKey("attachment.id"), primary_key=True)
)
