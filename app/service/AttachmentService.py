from model.Attachments import Attachment
from repository.AttachmentsRepository import AttachmentsRepository


class AttachmentService:
	@staticmethod
	def _parse_attachment_entries(attachments_data):
		if attachments_data is None:
			return []
		if not isinstance(attachments_data, list):
			raise ValueError("attachments must be an array")

		normalized = []
		for item in attachments_data:
			if isinstance(item, str):
				text = item.strip()
				if not text:
					raise ValueError("attachments cannot contain empty text values")
				normalized.append(text)
			elif isinstance(item, bool) or not isinstance(item, int):
				raise ValueError("attachments must contain strings or integer IDs")
			else:
				normalized.append(item)

		# Preserve order while removing exact duplicates.
		return list(dict.fromkeys(normalized))

	@staticmethod
	def _normalize_creator_id(created_by):
		if isinstance(created_by, str):
			if not created_by.isdigit():
				raise ValueError("Invalid creator identity")
			return int(created_by)
		if isinstance(created_by, bool) or not isinstance(created_by, int):
			raise ValueError("Invalid creator identity")
		return created_by

	@staticmethod
	def attach_to_task(task, attachments_data, created_by):
		entries = AttachmentService._parse_attachment_entries(attachments_data)
		if not entries:
			return []

		attachment_ids = [entry for entry in entries if isinstance(entry, int)]
		attachment_texts = [entry for entry in entries if isinstance(entry, str)]

		if attachment_ids:
			existing_attachments = AttachmentsRepository.get_by_ids(attachment_ids)
			attachment_by_id = {attachment.id: attachment for attachment in existing_attachments}
			missing_ids = [attachment_id for attachment_id in attachment_ids if attachment_id not in attachment_by_id]
			if missing_ids:
				raise ValueError(f"Invalid attachment IDs: {missing_ids}")

			for attachment_id in attachment_ids:
				attachment = attachment_by_id[attachment_id]
				if attachment not in task.attachments:
					task.attachments.append(attachment)

		if attachment_texts:
			creator_id = AttachmentService._normalize_creator_id(created_by)
			for text in attachment_texts:
				attachment = Attachment(text=text, created_by=creator_id)
				AttachmentsRepository.create(attachment, commit=False)
				task.attachments.append(attachment)

		return task.attachments
