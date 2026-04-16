from model.Priority import Priority
from extensions.db import db

def seed_priority():
    priorities = {
        "Low": "#00A63E",
        "Medium": "#F0B100",
        "High": "#FE9A00",
        "Critical": "#FF0000"
    }

    for name, color in priorities.items():
        existing = Priority.query.filter_by(name=name).first()
        if not existing:
            db.session.add(Priority(name=name, color=color))
            print(f"Seeded priority: {name} ({color})")

    db.session.commit()
