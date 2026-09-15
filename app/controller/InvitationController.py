from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from repository.UserRepository import UserRepository
from service.InvitationService import InvitationService
from utils.dto import invitation_to_dto

invitation_bp = Blueprint("invitation", __name__, url_prefix="/api/invitations")


def _current_user():
    user_id = int(get_jwt_identity())
    return UserRepository.find_by_id(user_id)


@invitation_bp.post("")
@jwt_required()
def create_invitation():
    user = _current_user()
    data = request.get_json(silent=True) or {}

    invitation, error = InvitationService.create_invitation(
        user, data.get("email"), data.get("role"), data.get("team_id")
    )
    if error:
        return jsonify({"error": error}), 400
    return jsonify(invitation_to_dto(invitation)), 201


@invitation_bp.get("")
@jwt_required()
def list_invitations():
    user = _current_user()
    invitations = InvitationService.list_invitations(user)
    return jsonify([invitation_to_dto(i) for i in invitations])


@invitation_bp.post("/<int:invitation_id>/resend")
@jwt_required()
def resend_invitation(invitation_id):
    user = _current_user()
    invitation, error = InvitationService.resend_invitation(user, invitation_id)
    if error:
        status = 404 if error == "Invitation not found" else 400
        return jsonify({"error": error}), status
    return jsonify(invitation_to_dto(invitation))


@invitation_bp.delete("/<int:invitation_id>")
@jwt_required()
def revoke_invitation(invitation_id):
    user = _current_user()
    ok, error = InvitationService.revoke_invitation(user, invitation_id)
    if not ok:
        status = 404 if error == "Invitation not found" else 403
        return jsonify({"error": error}), status
    return jsonify({"success": True})


# ---- Public endpoints used by the signup-via-invite page ----

@invitation_bp.get("/<string:token>")
def preview_invitation(token):
    data, error = InvitationService.preview_invitation(token)
    if error:
        return jsonify({"error": error}), 404
    return jsonify(data)


@invitation_bp.post("/<string:token>/accept")
def accept_invitation(token):
    data = request.get_json(silent=True) or {}
    missing = [f for f in ("name", "password") if not data.get(f)]
    if missing:
        return jsonify({"error": f"Missing required fields: {', '.join(missing)}"}), 400

    result, error = InvitationService.accept_invitation(token, data["name"], data["password"])
    if error:
        return jsonify({"error": error}), 400
    return jsonify(result), 201
