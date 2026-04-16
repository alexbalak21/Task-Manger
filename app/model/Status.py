from extensions.db import db

class Status(db.Model):
    __tablename__ = "status"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    color = db.Column(db.String(7), nullable=True)  # Hex color, e.g. #2B7FFF

    # Optional reverse relationship
    tasks = db.relationship("Task", back_populates="status_obj")

    def __repr__(self):
        return f"<Status {self.name} {self.color}>"
