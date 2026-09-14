from extensions.db import db
from datetime import datetime, timezone


class TeamInviteCode(db.Model):
    __tablename__ = "team_invite_code"

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(12), unique=True, nullable=False)
    team_id = db.Column(db.Integer, db.ForeignKey("team.id"), nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)

    created_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc)
    )

    team = db.relationship("Team", back_populates="invite_codes")

    def __repr__(self):
        return f"<TeamInviteCode {self.code} team={self.team_id} active={self.is_active}>"
