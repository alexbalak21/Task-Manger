from extensions.db import db

class Priority(db.Model):
    __tablename__ = "priority"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

    # Optional: reverse relationship
    tasks = db.relationship("Task", back_populates="priority_obj")

    def __repr__(self):
        return f"<Priority {self.name}>"
