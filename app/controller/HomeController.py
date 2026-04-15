from flask import Blueprint, send_from_directory, current_app as app
from pathlib import Path

home_blueprint = Blueprint("home", __name__)

# Serve static files (JS, CSS, images)
@home_blueprint.route("/assets/<path:filename>")
def assets(filename):
    return send_from_directory(Path(app.static_folder) / "assets", filename)

# SPA fallback: any non-API route → index.html
@home_blueprint.route("/", defaults={"path": ""})
@home_blueprint.route("/<path:path>")
def catch_all(path):
    # If the request starts with /api → do NOT serve React
    if path.startswith("api"):
        return {"error": "Not found"}, 404

    # Otherwise return React app
    return send_from_directory(app.static_folder, "index.html")
