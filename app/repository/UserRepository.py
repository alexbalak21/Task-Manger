from model.User import User
from extensions.db import db


class UserRepository:

    @staticmethod
    def find_by_email(email):
        return User.query.filter_by(email=email).first()

    @staticmethod
    def find_by_id(user_id):
        return User.query.get(user_id)

    @staticmethod
    def get_all():
        return User.query.all()

    @staticmethod
    def save(user):
        db.session.add(user)
        db.session.commit()
        return user

    @staticmethod
    def get_all_basic():
        users = User.query.with_entities(
            User.id,
            User.name,
            User.email
        ).all()
        return [
            {"id": u.id, "name": u.name, "email": u.email}
            for u in users]