from flask import Blueprint, request, jsonify
from service.AuthService import AuthService
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token, create_refresh_token

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")


@auth_bp.post("/register")
def register():
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

    result, error = AuthService.register(
        data["name"], data["email"], data["password"], profile_image
    )
    if error:
        return jsonify({"error": error}), 400
    return jsonify(result), 201


@auth_bp.post("/login")
def login():
    data = request.json
    result, error = AuthService.login(data["email"], data["password"])
    if error:
        return jsonify({"error": error}), 401
    return jsonify(result)


@auth_bp.post("/refresh")
def refresh():
    refresh_token = request.json.get("refresh_token")
    if not refresh_token:
        return jsonify({"error": "Missing refresh token"}), 401
    
    try:
        from flask_jwt_extended import decode_token
        payload = decode_token(refresh_token)
        user_id = payload.get("sub")
        
        access = create_access_token(identity=user_id)
        new_refresh = create_refresh_token(identity=user_id)
        return jsonify({"access_token": access, "refresh_token": new_refresh})
    except Exception as e:
        return jsonify({"error": "Invalid refresh token"}), 401


@auth_bp.post("/logout")
@jwt_required()
def logout():
    return jsonify({"message": "Successfully logged out"}), 200
