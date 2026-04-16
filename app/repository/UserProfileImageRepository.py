from extensions.db import db
from model.UserProfileImage import UserProfileImage


class UserProfileImageRepository:

    @staticmethod
    def find_all():
        return UserProfileImage.query.all()

    @staticmethod
    def delete(profile_image):
        db.session.delete(profile_image)
        db.session.commit()

    @staticmethod
    def find_by_user_id(user_id):
        return UserProfileImage.query.filter_by(user_id=user_id).first()

    @staticmethod
    def save(profile_image):
        db.session.add(profile_image)
        db.session.commit()
        return profile_image
