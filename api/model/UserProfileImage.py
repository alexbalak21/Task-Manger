from extensions.db import db
from sqlalchemy.dialects.mysql import MEDIUMBLOB


class UserProfileImage(db.Model):
    __tablename__ = "user_profile_images"

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), primary_key=True)
    blob = db.Column(MEDIUMBLOB, nullable=False)
