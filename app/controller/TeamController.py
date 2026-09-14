from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from repository.UserRepository import UserRepository
from service.TeamService import TeamService
from utils.dto import team_to_dto, team_member_to_dto, invite_code_to_dto

team_bp = Blueprint("team", __name__, url_prefix="/api/teams")


def _current_user():
    user_id = int(get_jwt_identity())
    return UserRepository.find_by_id(user_id)


def _error_status(error, not_found_msg="Team not found"):
    return 404 if error == not_found_msg else 403


@team_bp.post("")
@jwt_required()
def create_team():
    user = _current_user()
    data = request.get_json(silent=True) or {}

    team, error = TeamService.create_team(user, data.get("name"), data.get("description"))
    if error:
        return jsonify({"error": error}), 400
    return jsonify(team_to_dto(team)), 201


@team_bp.get("")
@jwt_required()
def list_teams():
    user = _current_user()
    teams = TeamService.list_teams(user)
    return jsonify([team_to_dto(t) for t in teams])


@team_bp.get("/<int:team_id>")
@jwt_required()
def get_team(team_id):
    user = _current_user()
    team, error = TeamService.get_team(user, team_id)
    if error:
        return jsonify({"error": error}), _error_status(error)
    return jsonify(team_to_dto(team, include_members=True))


@team_bp.put("/<int:team_id>")
@jwt_required()
def update_team(team_id):
    user = _current_user()
    data = request.get_json(silent=True) or {}

    team, error = TeamService.update_team(user, team_id, data)
    if error:
        return jsonify({"error": error}), _error_status(error)
    return jsonify(team_to_dto(team))


@team_bp.delete("/<int:team_id>")
@jwt_required()
def delete_team(team_id):
    user = _current_user()
    ok, error = TeamService.delete_team(user, team_id)
    if not ok:
        return jsonify({"error": error}), _error_status(error)
    return jsonify({"success": True})


@team_bp.post("/<int:team_id>/members")
@jwt_required()
def add_member(team_id):
    user = _current_user()
    data = request.get_json(silent=True) or {}
    member_user_id = data.get("user_id")

    if not member_user_id:
        return jsonify({"error": "user_id is required"}), 400

    link, error = TeamService.add_member(user, team_id, member_user_id)
    if error:
        status = 404 if error in ("Team not found", "User not found") else 400
        return jsonify({"error": error}), status
    return jsonify(team_member_to_dto(link)), 201


@team_bp.delete("/<int:team_id>/members/<int:member_user_id>")
@jwt_required()
def remove_member(team_id, member_user_id):
    user = _current_user()
    ok, error = TeamService.remove_member(user, team_id, member_user_id)
    if not ok:
        status = 404 if error in ("Team not found", "User is not a member of this team") else 403
        return jsonify({"error": error}), status
    return jsonify({"success": True})


@team_bp.get("/<int:team_id>/invite-code")
@jwt_required()
def get_invite_code(team_id):
    user = _current_user()
    invite, error = TeamService.get_or_create_invite_code(user, team_id)
    if error:
        return jsonify({"error": error}), _error_status(error)
    return jsonify(invite_code_to_dto(invite))


@team_bp.post("/<int:team_id>/invite-code/regenerate")
@jwt_required()
def regenerate_invite_code(team_id):
    user = _current_user()
    invite, error = TeamService.regenerate_invite_code(user, team_id)
    if error:
        return jsonify({"error": error}), _error_status(error)
    return jsonify(invite_code_to_dto(invite))
