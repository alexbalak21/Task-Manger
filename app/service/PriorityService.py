from model.Priority import Priority
from extensions.db import db

class PriorityService:
    @staticmethod
    def get_all():
        return Priority.query.all()

    @staticmethod
    def get_by_id(priority_id):
        return Priority.query.get(priority_id)

    @staticmethod
    def create(data):
        if not data or "name" not in data:
            raise ValueError("'name' is required")
        if Priority.query.filter_by(name=data["name"]).first():
            raise ValueError("Priority with this name already exists")
        color = data.get("color")
        priority = Priority(name=data["name"], color=color)
        db.session.add(priority)
        db.session.commit()
        return priority

    @staticmethod
    def update(priority, data):
        if "name" in data:
            if Priority.query.filter(Priority.name == data["name"], Priority.id != priority.id).first():
                raise ValueError("Priority with this name already exists")
            priority.name = data["name"]
        if "color" in data:
            priority.color = data["color"]
        db.session.commit()
        return priority

    @staticmethod
    def delete(priority):
        db.session.delete(priority)
        db.session.commit()
