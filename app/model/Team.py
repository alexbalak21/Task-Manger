from extensions.db import db
from datetime import datetime, timezone


class Team(db.Model):
    __tablename__ = "team"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(255), nullable=True)

    # The manager (or admin) who owns/manages this team
    created_by = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    created_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc)
    )
    updated_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc)
    )

    manager = db.relationship("User", foreign_keys=[created_by])
    members = db.relationship("TeamMember", back_populates="team", cascade="all, delete-orphan")
    invite_codes = db.relationship("TeamInviteCode", back_populates="team", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Team {self.name}>"
