from model.Status import Status
from extensions.db import db

def seed_status():
    statuses = [
        {"name": "Pending", "color": "#F0B100"},
        {"name": "Awaiting", "color": "#FE9A00"},
        {"name": "In Progress", "color": "#2B7FFF"},
        {"name": "Completed", "color": "#00A63E"},
    ]

    for status in statuses:
        existing = Status.query.filter_by(name=status["name"]).first()
        if not existing:
            db.session.add(Status(name=status["name"], color=status["color"]))
            print(f"Seeded status: {status['name']} ({status['color']})")

    db.session.commit()
