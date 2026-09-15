from model.UserInvitation import UserInvitation
from extensions.db import db


class InvitationRepository:

    @staticmethod
    def find_by_id(invitation_id):
        return UserInvitation.query.get(invitation_id)

    @staticmethod
    def find_by_token(token):
        return UserInvitation.query.filter_by(token=token).first()

    @staticmethod
    def find_pending_by_email(email):
        return UserInvitation.query.filter_by(email=email, status="pending").first()

    @staticmethod
    def get_by_inviter(inviter_id):
        return UserInvitation.query.filter_by(invited_by=inviter_id).order_by(
            UserInvitation.created_at.desc()
        ).all()

    @staticmethod
    def get_all():
        return UserInvitation.query.order_by(UserInvitation.created_at.desc()).all()

    @staticmethod
    def save(invitation):
        db.session.add(invitation)
        db.session.commit()
        return invitation

    @staticmethod
    def delete(invitation):
        db.session.delete(invitation)
        db.session.commit()
