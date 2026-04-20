from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from service.TaskService import TaskService
from middleware.admin_required import admin_required

task_bp = Blueprint("task", __name__, url_prefix="/api/tasks")

# GET all tasks
@task_bp.get("")
@jwt_required()
def get_tasks():
	tasks = TaskService.get_all()
	return jsonify([task_to_dto(t) for t in tasks])

# GET single task
@task_bp.get("/<int:task_id>")
@jwt_required()
def get_task(task_id):
	task = TaskService.get_by_id(task_id)
	if not task:
		return jsonify({"error": "Task not found"}), 404
	return jsonify(task_to_dto(task))

# CREATE task (admin only)
@task_bp.post("")
@admin_required
def create_task():
	data = request.get_json(silent=True) or {}
	creator_id = get_jwt_identity()
	try:
		task = TaskService.create(data, created_by=creator_id)
	except ValueError as err:
		return jsonify({"error": str(err)}), 400
	return jsonify(task_to_dto(task)), 201

# UPDATE task
@task_bp.put("/<int:task_id>")
@jwt_required()
def update_task(task_id):
	task = TaskService.get_by_id(task_id)
	if not task:
		return jsonify({"error": "Task not found"}), 404
	data = request.json
	try:
		updated = TaskService.update(task, data)
	except ValueError as err:
		return jsonify({"error": str(err)}), 400
	return jsonify(task_to_dto(updated))

# DELETE task (admin only)
@task_bp.delete("/<int:task_id>")
@admin_required
def delete_task(task_id):
	task = TaskService.get_by_id(task_id)
	if not task:
		return jsonify({"error": "Task not found"}), 404
	TaskService.delete(task)
	return jsonify({"message": "Task deleted"})

# Helper: Task to DTO
def task_to_dto(task):
	return {
		"id": task.id,
		"title": task.title,
		"description": task.description,
		"priority_id": task.priority_id,
		"status_id": task.status_id,
		"start_date": task.start_date.isoformat() if task.start_date else None,
		"due_date": task.due_date.isoformat() if task.due_date else None,
		"users": [user.id for user in task.users],
		"todos": [todo.id for todo in task.todos],
		"attachments": [attachment.id for attachment in task.attachments],
		"created_at": task.created_at.isoformat() if task.created_at else None,
		"updated_at": task.updated_at.isoformat() if task.updated_at else None
	}
