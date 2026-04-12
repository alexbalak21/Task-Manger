from model.Priority import Priority
from extensions.db import db

def seed_priority():
    priorities = ["Low", "Medium", "High"]

    for name in priorities:
        existing = Priority.query.filter_by(name=name).first()
        if not existing:
            db.session.add(Priority(name=name))
            print(f"Seeded priority: {name}")

    db.session.commit()
