
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from service.StatusService import StatusService
from middleware.admin_required import admin_required

status_bp = Blueprint("status", __name__, url_prefix="/api/statuses")

# GET all statuses
@status_bp.get("")
@jwt_required()
def get_statuses():
	statuses = StatusService.get_all()
	return jsonify([status_to_dto(s) for s in statuses])

# GET single status
@status_bp.get("/<int:status_id>")
@jwt_required()
def get_status(status_id):
	status = StatusService.get_by_id(status_id)
	if not status:
		return jsonify({"error": "Status not found"}), 404
	return jsonify(status_to_dto(status))

# CREATE status (admin only)
@status_bp.post("")
@admin_required
def create_status():
	data = request.json
	try:
		status = StatusService.create(data)
	except ValueError as err:
		return jsonify({"error": str(err)}), 400
	return jsonify(status_to_dto(status)), 201

# UPDATE status
@status_bp.put("/<int:status_id>")
@admin_required
def update_status(status_id):
	status = StatusService.get_by_id(status_id)
	if not status:
		return jsonify({"error": "Status not found"}), 404
	data = request.json
	try:
		updated = StatusService.update(status, data)
	except ValueError as err:
		return jsonify({"error": str(err)}), 400
	return jsonify(status_to_dto(updated))

# DELETE status (admin only)
@status_bp.delete("/<int:status_id>")
@admin_required
def delete_status(status_id):
	status = StatusService.get_by_id(status_id)
	if not status:
		return jsonify({"error": "Status not found"}), 404
	StatusService.delete(status)
	return jsonify({"message": "Status deleted"})

def status_to_dto(status):
	return {
		"id": status.id,
		"name": status.name
	}
