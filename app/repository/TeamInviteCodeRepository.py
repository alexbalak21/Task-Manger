from model.TeamInviteCode import TeamInviteCode
from extensions.db import db


class TeamInviteCodeRepository:

    @staticmethod
    def find_active_by_code(code):
        return TeamInviteCode.query.filter_by(code=code, is_active=True).first()

    @staticmethod
    def get_active_for_team(team_id):
        return TeamInviteCode.query.filter_by(team_id=team_id, is_active=True).first()

    @staticmethod
    def save(invite_code):
        db.session.add(invite_code)
        db.session.commit()
        return invite_code
