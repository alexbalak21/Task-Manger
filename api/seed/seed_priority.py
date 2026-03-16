from model.Status import Status
from extensions.db import db

def seed_status():
    statuses = ["Todo", "In Progress", "Completed", "Blocked"]

    for name in statuses:
        existing = Status.query.filter_by(name=name).first()
        if not existing:
            db.session.add(Status(name=name))
            print(f"Seeded status: {name}")

    db.session.commit()
