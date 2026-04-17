from model.Attachments import Attachment
from extensions.db import db


class AttachmentsRepository:
	@staticmethod
	def get_by_id(attachment_id):
		return Attachment.query.get(attachment_id)

	@staticmethod
	def get_by_ids(attachment_ids):
		if not attachment_ids:
			return []
		return Attachment.query.filter(Attachment.id.in_(attachment_ids)).all()

	@staticmethod
	def create(attachment, commit=True):
		db.session.add(attachment)
		if commit:
			db.session.commit()
		return attachment
