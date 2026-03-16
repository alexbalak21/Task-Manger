from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from service.UserService import UserService
from repository.UserRepository import UserRepository

user_bp = Blueprint("user", __name__, url_prefix="/api/user")


@user_bp.get("")
@jwt_required()
def get_user():
    user_id = int(get_jwt_identity())
    return jsonify(UserService.get_user(user_id))


@user_bp.put("")
@jwt_required()
def update_user():
    user_id = int(get_jwt_identity())
    data = request.json
    return jsonify(UserService.update_user(user_id, data))


@user_bp.post("/password")
@jwt_required()
def change_password():
    user_id = int(get_jwt_identity())
    user = UserRepository.find_by_id(user_id)

    data = request.json
    ok, msg = UserService.change_password(
        user, data["currentPassword"], data["newPassword"]
    )
    if not ok:
        return jsonify({"error": msg}), 400

    return jsonify({"success": True, "message": msg})
