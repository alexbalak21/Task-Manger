from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from service.TodoService import TodoService
from repository.UserRepository import UserRepository

todo_bp = Blueprint("todo", __name__, url_prefix="/api/todos")
todo_api_bp = Blueprint("todo_api", __name__, url_prefix="/api")

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

# GET all todos
@todo_bp.get("")
@jwt_required()
def get_todos():
	todos = TodoService.get_all()
	return jsonify([todo_to_dto(t) for t in todos])

# GET todos by task
@todo_bp.get("/task/<int:task_id>")
@jwt_required()
def get_todos_by_task(task_id):
	todos = TodoService.get_by_task_id(task_id)
	return jsonify([todo_to_dto(t) for t in todos])

# GET todos by ids from JSON body
@todo_api_bp.get("/todo/ids")
@jwt_required()
def get_todos_by_ids():
	data = request.get_json(silent=True) or {}
	todo_ids = data.get("todos_ids")
	if not isinstance(todo_ids, list):
		return jsonify({"error": "todos must be a list of todo IDs"}), 400

	try:
		todo_ids = [int(todo_id) for todo_id in todo_ids]
	except (TypeError, ValueError):
		return jsonify({"error": "todos must contain only integer IDs"}), 400

	todos = TodoService.get_by_ids(todo_ids)
	return jsonify([todo_to_dto(t) for t in todos])

# GET single todo
@todo_bp.get("/<int:todo_id>")
@jwt_required()
def get_todo(todo_id):
	todo = TodoService.get_by_id(todo_id)
	if not todo:
		return jsonify({"error": "Todo not found"}), 404
	return jsonify(todo_to_dto(todo))

# CREATE todo
@todo_bp.post("")
@admin_required
def create_todo():
	data = request.json
	try:
		todo = TodoService.create(data)
	except ValueError as err:
		return jsonify({"error": str(err)}), 400
	return jsonify(todo_to_dto(todo)), 201

# UPDATE todo
@todo_bp.put("/<int:todo_id>")
@jwt_required()
def update_todo(todo_id):
	todo = TodoService.get_by_id(todo_id)
	if not todo:
		return jsonify({"error": "Todo not found"}), 404
	data = request.json
	try:
		updated = TodoService.update(todo, data)
	except ValueError as err:
		return jsonify({"error": str(err)}), 400
	return jsonify(todo_to_dto(updated))

# DELETE todo (admin only)
@todo_bp.delete("/<int:todo_id>")
@admin_required
def delete_todo(todo_id):
	todo = TodoService.get_by_id(todo_id)
	if not todo:
		return jsonify({"error": "Todo not found"}), 404
	TodoService.delete(todo)
	return jsonify({"message": "Todo deleted"})

# Helper: Todo to DTO
def todo_to_dto(todo):
	return {
		"id": todo.id,
		"text": todo.text,
		"in_progress": todo.in_progress,
		"completed": todo.completed,
		"worked_by": todo.worked_by,
		"completed_at": todo.completed_at.isoformat() if todo.completed_at else None,
		"task_id": todo.task_id,
		"created_at": todo.created_at.isoformat() if todo.created_at else None,
		"updated_at": todo.updated_at.isoformat() if todo.updated_at else None
	}
