import secrets
from datetime import datetime, timezone

from flask import current_app
from flask_jwt_extended import create_access_token, create_refresh_token

from repository.InvitationRepository import InvitationRepository
from repository.UserRepository import UserRepository
from repository.TeamRepository import TeamRepository
from model.UserInvitation import UserInvitation
from model.User import User
from utils.dto import user_to_dto
from service.EmailService import EmailService


class InvitationService:

    @staticmethod
    def create_invitation(inviter, email, role, team_id=None):
        if inviter.role not in ("admin", "manager"):
            return None, "Not authorized to invite users"

        role = (role or "member").strip().lower()
        if role not in ("admin", "manager", "member"):
            return None, "Invalid role"
        if inviter.role == "manager" and role != "member":
            return None, "Managers can only invite members"

        email = (email or "").strip().lower()
        if not email:
            return None, "Email is required"

        if UserRepository.find_by_email(email):
            return None, "A user with this email already exists"

        existing = InvitationRepository.find_pending_by_email(email)
        if existing and not existing.is_expired():
            return None, "There is already a pending invitation for this email"

        team = None
        if team_id:
            team = TeamRepository.find_by_id(team_id)
            if not team:
                return None, "Team not found"
            can_assign_team = inviter.role == "admin" or team.created_by == inviter.id
            if not can_assign_team:
                return None, "You do not have permission to invite into this team"

        invitation = UserInvitation(
            email=email,
            role=role,
            team_id=team.id if team else None,
            invited_by=inviter.id,
            token=secrets.token_urlsafe(32),
        )
        InvitationRepository.save(invitation)

        InvitationService._send(invitation, inviter)
        return invitation, None

    @staticmethod
    def _send(invitation, inviter):
        frontend_url = current_app.config.get("FRONTEND_URL", "").rstrip("/")
        invite_link = f"{frontend_url}/signup/invite/{invitation.token}"
        EmailService.send_invite_email(
            to_email=invitation.email,
            invite_link=invite_link,
            role=invitation.role,
            inviter_name=inviter.name,
            team_name=invitation.team.name if invitation.team else None,
        )

    @staticmethod
    def resend_invitation(user, invitation_id):
        invitation = InvitationRepository.find_by_id(invitation_id)
        if not invitation:
            return None, "Invitation not found"
        if not InvitationService._can_manage(user, invitation):
            return None, "You do not have permission to resend this invitation"
        if invitation.status != "pending":
            return None, "Only pending invitations can be resent"

        InvitationService._send(invitation, user)
        return invitation, None

    @staticmethod
    def revoke_invitation(user, invitation_id):
        invitation = InvitationRepository.find_by_id(invitation_id)
        if not invitation:
            return False, "Invitation not found"
        if not InvitationService._can_manage(user, invitation):
            return False, "You do not have permission to revoke this invitation"

        invitation.status = "revoked"
        InvitationRepository.save(invitation)
        return True, None

    @staticmethod
    def _can_manage(user, invitation):
        return user.role == "admin" or invitation.invited_by == user.id

    @staticmethod
    def list_invitations(user):
        if user.role == "admin":
            return InvitationRepository.get_all()
        return InvitationRepository.get_by_inviter(user.id)

    @staticmethod
    def preview_invitation(token):
        """Public: used by the signup page to prefill email/role/team."""
        invitation = InvitationRepository.find_by_token(token)
        if not invitation or invitation.status != "pending":
            return None, "This invitation link is invalid or has already been used"
        if invitation.is_expired():
            return None, "This invitation link has expired"

        return {
            "email": invitation.email,
            "role": invitation.role,
            "team_name": invitation.team.name if invitation.team else None,
        }, None

    @staticmethod
    def accept_invitation(token, name, password):
        invitation = InvitationRepository.find_by_token(token)
        if not invitation or invitation.status != "pending":
            return None, "This invitation link is invalid or has already been used"
        if invitation.is_expired():
            return None, "This invitation link has expired"
        if UserRepository.find_by_email(invitation.email):
            return None, "A user with this email already exists"

        user = User(name=name, email=invitation.email, role=invitation.role)
        user.set_password(password)
        UserRepository.save(user)

        if invitation.team_id:
            from repository.TeamMemberRepository import TeamMemberRepository
            from model.TeamMember import TeamMember
            TeamMemberRepository.save(TeamMember(team_id=invitation.team_id, user_id=user.id))

        invitation.status = "accepted"
        invitation.accepted_at = datetime.now(timezone.utc)
        InvitationRepository.save(invitation)

        access = create_access_token(identity=str(user.id))
        refresh = create_refresh_token(identity=str(user.id))

        return {
            "access_token": access,
            "refresh_token": refresh,
            "user": user_to_dto(user),
        }, None
