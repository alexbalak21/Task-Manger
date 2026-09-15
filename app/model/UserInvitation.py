from extensions.db import db
from datetime import datetime, timezone, timedelta


def _default_expiry():
    return datetime.now(timezone.utc) + timedelta(days=7)


class UserInvitation(db.Model):
    __tablename__ = "user_invitation"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), nullable=False)  # manager | member
    team_id = db.Column(db.Integer, db.ForeignKey("team.id"), nullable=True)

    token = db.Column(db.String(64), unique=True, nullable=False)
    status = db.Column(db.String(20), default="pending", nullable=False)  # pending|accepted|revoked|expired

    invited_by = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    expires_at = db.Column(db.DateTime, default=_default_expiry, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    accepted_at = db.Column(db.DateTime, nullable=True)

    team = db.relationship("Team")
    inviter = db.relationship("User", foreign_keys=[invited_by])

    def is_expired(self):
        expires_at = self.expires_at
        if expires_at.tzinfo is None:
            expires_at = expires_at.replace(tzinfo=timezone.utc)
        return datetime.now(timezone.utc) > expires_at

    def __repr__(self):
        return f"<UserInvitation {self.email} role={self.role} status={self.status}>"
