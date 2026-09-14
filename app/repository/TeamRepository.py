from model.Team import Team
from extensions.db import db


class TeamRepository:

    @staticmethod
    def find_by_id(team_id):
        return Team.query.get(team_id)

    @staticmethod
    def get_all():
        return Team.query.all()

    @staticmethod
    def get_by_manager(manager_id):
        return Team.query.filter_by(created_by=manager_id).all()

    @staticmethod
    def save(team):
        db.session.add(team)
        db.session.commit()
        return team

    @staticmethod
    def delete(team):
        db.session.delete(team)
        db.session.commit()
