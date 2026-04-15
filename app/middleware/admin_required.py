from functools import wraps

from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from repository.UserRepository import UserRepository

def admin_required(fn):
	@wraps(fn)
	@jwt_required()
	def wrapper(*args, **kwargs):
		user_id = get_jwt_identity()
		user = UserRepository.find_by_id(user_id)
		if not user or user.role != "admin":
			return jsonify({"error": "Admin access required"}), 403
		return fn(*args, **kwargs)
	return wrapper