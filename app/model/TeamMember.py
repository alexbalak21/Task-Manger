from extensions.db import db
from datetime import datetime, timezone


class TeamMember(db.Model):
    __tablename__ = "team_member"
    __table_args__ = (
        db.UniqueConstraint("team_id", "user_id", name="uq_team_user"),
    )

    id = db.Column(db.Integer, primary_key=True)
    team_id = db.Column(db.Integer, db.ForeignKey("team.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    joined_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc)
    )

    team = db.relationship("Team", back_populates="members")
    user = db.relationship("User")

    def __repr__(self):
        return f"<TeamMember team={self.team_id} user={self.user_id}>"
