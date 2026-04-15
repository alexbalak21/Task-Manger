from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from service.UserTaskService import UserTaskService
from repository.UserRepository import UserRepository
from repository.TaskRepository import TaskRepository

user_task_bp = Blueprint("user_task", __name__, url_prefix="/api/user-tasks")

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

# Assign user to task (admin only)
@user_task_bp.post("/assign")
@admin_required
def assign_user_to_task():
    data = request.json
    user_id = data.get("user_id")
    task_id = data.get("task_id")
    if not user_id or not task_id:
        return jsonify({"error": "user_id and task_id are required"}), 400
    try:
        UserTaskService.assign_user_to_task(user_id, task_id)
    except ValueError as err:
        return jsonify({"error": str(err)}), 404
    return jsonify({"success": True})

# Unassign user from task (admin only)
@user_task_bp.post("/unassign")
@admin_required
def unassign_user_from_task():
    data = request.json
    user_id = data.get("user_id")
    task_id = data.get("task_id")
    if not user_id or not task_id:
        return jsonify({"error": "user_id and task_id are required"}), 400
    try:
        UserTaskService.unassign_user_from_task(user_id, task_id)
    except ValueError as err:
        return jsonify({"error": str(err)}), 404
    return jsonify({"success": True})

# Get users for a task
@user_task_bp.get("/task/<int:task_id>")
@jwt_required()
def get_users_for_task(task_id):
    user_ids = UserTaskService.get_users_for_task(task_id)
    return jsonify({"user_ids": user_ids})

# Get tasks for a user
@user_task_bp.get("/user/<int:user_id>")
@jwt_required()
def get_tasks_for_user(user_id):
    task_ids = UserTaskService.get_tasks_for_user(user_id)
    return jsonify({"task_ids": task_ids})
