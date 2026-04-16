from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from service.PriorityService import PriorityService
from middleware.admin_required import admin_required

priority_bp = Blueprint("priority", __name__, url_prefix="/api/priorities")

# GET all priorities
@priority_bp.get("")
@jwt_required()
def get_priorities():
	priorities = PriorityService.get_all()
	return jsonify([priority_to_dto(p) for p in priorities])

# GET single priority
@priority_bp.get("/<int:priority_id>")
@jwt_required()
def get_priority(priority_id):
	priority = PriorityService.get_by_id(priority_id)
	if not priority:
		return jsonify({"error": "Priority not found"}), 404
	return jsonify(priority_to_dto(priority))

# CREATE priority (admin only)
@priority_bp.post("")
@admin_required
def create_priority():
	data = request.json
	try:
		priority = PriorityService.create(data)
	except ValueError as err:
		return jsonify({"error": str(err)}), 400
	return jsonify(priority_to_dto(priority)), 201

# UPDATE priority
@priority_bp.put("/<int:priority_id>")
@admin_required
def update_priority(priority_id):
	priority = PriorityService.get_by_id(priority_id)
	if not priority:
		return jsonify({"error": "Priority not found"}), 404
	data = request.json
	try:
		updated = PriorityService.update(priority, data)
	except ValueError as err:
		return jsonify({"error": str(err)}), 400
	return jsonify(priority_to_dto(updated))

# DELETE priority (admin only)
@priority_bp.delete("/<int:priority_id>")
@admin_required
def delete_priority(priority_id):
	priority = PriorityService.get_by_id(priority_id)
	if not priority:
		return jsonify({"error": "Priority not found"}), 404
	PriorityService.delete(priority)
	return jsonify({"message": "Priority deleted"})

def priority_to_dto(priority):
	return {
		"id": priority.id,
		"name": priority.name,
		"color": priority.color
	}
