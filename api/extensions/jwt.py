from flask_jwt_extended import JWTManager
from flask import jsonify

jwt = JWTManager()


# JWT Error Handlers
@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    return jsonify({"error": "Token has expired", "code": "token_expired"}), 401


@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({"error": "Invalid token", "code": "invalid_token"}), 401


@jwt.unauthorized_loader
def unauthorized_callback(error):
    return jsonify({"error": "Missing authorization header", "code": "missing_token"}), 401


@jwt.revoked_token_loader
def revoked_token_callback(jwt_header, jwt_payload):
    return jsonify({"error": "Token has been revoked", "code": "token_revoked"}), 401

