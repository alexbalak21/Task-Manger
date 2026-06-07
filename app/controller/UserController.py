from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from service.UserService import UserService
from repository.UserRepository import UserRepository
from middleware.admin_required import admin_required

user_bp = Blueprint("user", __name__, url_prefix="/api/")


@user_bp.get("user")
@jwt_required()
def get_user():
    user_id = int(get_jwt_identity())
    return jsonify(UserService.get_user(user_id))


@user_bp.put("user")
@jwt_required()
def update_user():
    user_id = int(get_jwt_identity())
    data = request.json
    return jsonify(UserService.update_user(user_id, data))


@user_bp.put("user/password")
@user_bp.post("user/password")
@jwt_required()
def change_password():
    user_id = int(get_jwt_identity())
    user = UserRepository.find_by_id(user_id)

    if not user:
        return jsonify({"error": "User not found"}), 404

    data = request.get_json(silent=True) or {}
    current_password = data.get("password") or data.get("currentPassword")
    new_password = data.get("new_password") or data.get("newPassword")

    if not current_password or not new_password:
        return jsonify({"error": "Missing required fields: password, new_password"}), 400

    ok, msg = UserService.change_password(user, current_password, new_password)
    if not ok:
        return jsonify({"error": msg}), 400

    return jsonify({"success": True, "message": msg})


@user_bp.get("users")
@jwt_required()
def get_all_users():
    return jsonify(UserService.get_all_users())


@user_bp.post("user/register")
def register_user():
    data = request.get_json(silent=True) or {}
    profile_image = None

    if request.content_type and request.content_type.startswith("multipart/form-data"):
        data = request.form
        uploaded_file = request.files.get("profile_image")
        if uploaded_file and uploaded_file.filename:
            profile_image = uploaded_file

    required_fields = ["name", "email", "password"]
    missing_fields = [field for field in required_fields if not data.get(field)]
    if missing_fields:
        return jsonify({"error": f"Missing required fields: {', '.join(missing_fields)}"}), 400

    ok, msg = UserService.register_user(data, profile_image)
    if not ok:
        return jsonify({"error": msg}), 400

    return jsonify({"success": True, "message": msg})


# UPLOAD USER PROFILE IMAGE
@user_bp.post("user/image")
@jwt_required()
def upload_profile_image():
    user_id = int(get_jwt_identity())
    if not request.content_type or not request.content_type.startswith("multipart/form-data"):
        return jsonify({"error": "Content-Type must be multipart/form-data"}), 400

    uploaded_file = request.files.get("profile_image")
    if not uploaded_file or not uploaded_file.filename:
        return jsonify({"error": "No profile_image file uploaded"}), 400

    ok, result = UserService.upload_profile_image(user_id, uploaded_file)
    if not ok:
        return jsonify({"error": result}), 400

    return jsonify(result)

# DELETE USER PROFILE IMAGE
@user_bp.delete("user/image")
@jwt_required()
def delete_profile_image():
    user_id = int(get_jwt_identity())
    ok, msg = UserService.delete_profile_image(user_id)
    if not ok:
        return jsonify({"error": msg}), 400
    return jsonify({"success": True, "message": msg})


@user_bp.put("user/name")
@jwt_required()
def update_name():
    user_id = int(get_jwt_identity())
    data = request.get_json(silent=True) or {}
    ok, result = UserService.update_name(user_id, data.get("name"))
    if not ok:
        return jsonify({"error": result}), 400
    return jsonify(result)


@user_bp.put("user/email")
@jwt_required()
def update_email():
    user_id = int(get_jwt_identity())
    data = request.get_json(silent=True) or {}
    ok, result = UserService.update_email(user_id, data.get("email"))
    if not ok:
        return jsonify({"error": result}), 400
    return jsonify(result)