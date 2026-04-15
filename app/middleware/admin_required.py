from flask_jwt_extended import jwt_required, get_jwt_identity

def admin_required(fn):
	@jwt_required()
	def wrapper(*args, **kwargs):
		user_id = get_jwt_identity()
		user = UserRepository.find_by_id(user_id)
		if not user or user.role != "admin":
			return jsonify({"error": "Admin access required"}), 403
		return fn(*args, **kwargs)
	wrapper.__name__ = fn.__name__
	return wrapper