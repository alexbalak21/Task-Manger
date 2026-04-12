from model.Status import Status
from extensions.db import db

def seed_status():
    # "Pending", "Awaiting", "In Progress", "On Hold", "Completed", "Cancelled"
    statuses = ["Pending", "In Progress" "Completed"]

    for name in statuses:
        existing = Status.query.filter_by(name=name).first()
        if not existing:
            db.session.add(Status(name=name))
            print(f"Seeded status: {name}")

    db.session.commit()
