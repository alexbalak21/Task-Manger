from functools import wraps
from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from repository.UserRepository import UserRepository


def roles_required(*allowed_roles):
    """Restrict a route to one or more roles, e.g. @roles_required('admin', 'manager')."""
    def decorator(fn):
        @wraps(fn)
        @jwt_required()
        def wrapper(*args, **kwargs):
            user_id = get_jwt_identity()
            user = UserRepository.find_by_id(user_id)
            if not user or user.role not in allowed_roles:
                return jsonify({
                    "error": f"Requires one of the following roles: {', '.join(allowed_roles)}"
                }), 403
            return fn(*args, **kwargs)
        return wrapper
    return decorator
