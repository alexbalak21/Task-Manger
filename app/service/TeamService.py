import secrets
import string

from repository.TeamRepository import TeamRepository
from repository.TeamMemberRepository import TeamMemberRepository
from repository.TeamInviteCodeRepository import TeamInviteCodeRepository
from repository.UserRepository import UserRepository
from model.Team import Team
from model.TeamMember import TeamMember
from model.TeamInviteCode import TeamInviteCode


def _generate_code(length=8):
    alphabet = string.ascii_uppercase + string.digits
    while True:
        code = "".join(secrets.choice(alphabet) for _ in range(length))
        if not TeamInviteCodeRepository.find_active_by_code(code):
            return code


class TeamService:

    @staticmethod
    def _can_manage(user, team):
        """Admins manage every team. Managers only manage teams they created."""
        return user.role == "admin" or (user.role == "manager" and team.created_by == user.id)

    # ---------------- Teams ----------------

    @staticmethod
    def create_team(creator, name, description=None):
        if creator.role not in ("admin", "manager"):
            return None, "Only admins and managers can create teams"

        name = (name or "").strip()
        if not name:
            return None, "Team name is required"

        team = Team(name=name, description=(description or "").strip() or None, created_by=creator.id)
        TeamRepository.save(team)
        return team, None

    @staticmethod
    def list_teams(user):
        if user.role == "admin":
            return TeamRepository.get_all()
        if user.role == "manager":
            return TeamRepository.get_by_manager(user.id)
        # member: only teams they belong to
        memberships = TeamMemberRepository.get_by_user(user.id)
        return [m.team for m in memberships]

    @staticmethod
    def get_team(user, team_id):
        team = TeamRepository.find_by_id(team_id)
        if not team:
            return None, "Team not found"
        if TeamService._can_manage(user, team):
            return team, None
        if TeamMemberRepository.find(team_id, user.id):
            return team, None
        return None, "You do not have access to this team"

    @staticmethod
    def update_team(user, team_id, data):
        team = TeamRepository.find_by_id(team_id)
        if not team:
            return None, "Team not found"
        if not TeamService._can_manage(user, team):
            return None, "You do not have permission to update this team"

        if data.get("name"):
            team.name = data["name"].strip()
        if "description" in data:
            team.description = data["description"]

        TeamRepository.save(team)
        return team, None

    @staticmethod
    def delete_team(user, team_id):
        team = TeamRepository.find_by_id(team_id)
        if not team:
            return False, "Team not found"
        if not TeamService._can_manage(user, team):
            return False, "You do not have permission to delete this team"

        TeamRepository.delete(team)
        return True, None

    # ---------------- Membership ----------------

    @staticmethod
    def add_member(user, team_id, member_user_id):
        team = TeamRepository.find_by_id(team_id)
        if not team:
            return None, "Team not found"
        if not TeamService._can_manage(user, team):
            return None, "You do not have permission to modify this team"

        member = UserRepository.find_by_id(member_user_id)
        if not member:
            return None, "User not found"
        if member.role != "member":
            return None, "Only members can be added to a team"

        if TeamMemberRepository.find(team_id, member_user_id):
            return None, "User is already a member of this team"

        link = TeamMember(team_id=team_id, user_id=member_user_id)
        TeamMemberRepository.save(link)
        return link, None

    @staticmethod
    def remove_member(user, team_id, member_user_id):
        team = TeamRepository.find_by_id(team_id)
        if not team:
            return False, "Team not found"
        if not TeamService._can_manage(user, team):
            return False, "You do not have permission to modify this team"

        link = TeamMemberRepository.find(team_id, member_user_id)
        if not link:
            return False, "User is not a member of this team"

        TeamMemberRepository.delete(link)
        return True, None

    # ---------------- Invite codes ----------------

    @staticmethod
    def get_or_create_invite_code(user, team_id):
        team = TeamRepository.find_by_id(team_id)
        if not team:
            return None, "Team not found"
        if not TeamService._can_manage(user, team):
            return None, "You do not have permission to view this team's invite code"

        existing = TeamInviteCodeRepository.get_active_for_team(team_id)
        if existing:
            return existing, None

        invite = TeamInviteCode(code=_generate_code(), team_id=team_id, created_by=user.id)
        TeamInviteCodeRepository.save(invite)
        return invite, None

    @staticmethod
    def regenerate_invite_code(user, team_id):
        team = TeamRepository.find_by_id(team_id)
        if not team:
            return None, "Team not found"
        if not TeamService._can_manage(user, team):
            return None, "You do not have permission to modify this team's invite code"

        existing = TeamInviteCodeRepository.get_active_for_team(team_id)
        if existing:
            existing.is_active = False
            TeamInviteCodeRepository.save(existing)

        invite = TeamInviteCode(code=_generate_code(), team_id=team_id, created_by=user.id)
        TeamInviteCodeRepository.save(invite)
        return invite, None

    @staticmethod
    def redeem_invite_code(code):
        """Used during member self-registration. Returns (team, error)."""
        clean_code = (code or "").strip().upper()
        if not clean_code:
            return None, "An invite code is required"

        invite = TeamInviteCodeRepository.find_active_by_code(clean_code)
        if not invite:
            return None, "Invalid or expired invite code"

        return invite.team, None
