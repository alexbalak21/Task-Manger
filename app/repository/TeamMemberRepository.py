from model.TeamMember import TeamMember
from extensions.db import db


class TeamMemberRepository:

    @staticmethod
    def find(team_id, user_id):
        return TeamMember.query.filter_by(team_id=team_id, user_id=user_id).first()

    @staticmethod
    def get_by_team(team_id):
        return TeamMember.query.filter_by(team_id=team_id).all()

    @staticmethod
    def get_by_user(user_id):
        return TeamMember.query.filter_by(user_id=user_id).all()

    @staticmethod
    def save(team_member):
        db.session.add(team_member)
        db.session.commit()
        return team_member

    @staticmethod
    def delete(team_member):
        db.session.delete(team_member)
        db.session.commit()
