from model.Status import Status
from extensions.db import db

class StatusService:
    @staticmethod
    def get_all():
        return Status.query.all()

    @staticmethod
    def get_by_id(status_id):
        return Status.query.get(status_id)

    @staticmethod
    def create(data):
        if not data or "name" not in data:
            raise ValueError("'name' is required")
        if Status.query.filter_by(name=data["name"]).first():
            raise ValueError("Status with this name already exists")
        color = data.get("color")
        status = Status(name=data["name"], color=color)
        db.session.add(status)
        db.session.commit()
        return status

    @staticmethod
    def update(status, data):
        if "name" in data:
            if Status.query.filter(Status.name == data["name"], Status.id != status.id).first():
                raise ValueError("Status with this name already exists")
            status.name = data["name"]
        if "color" in data:
            status.color = data["color"]
        db.session.commit()
        return status

    @staticmethod
    def delete(status):
        db.session.delete(status)
        db.session.commit()
