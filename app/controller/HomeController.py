from flask import Blueprint, send_from_directory, current_app as app

home_blueprint = Blueprint("home", __name__)

@home_blueprint.route("/")
def home():
    print(f"Serving index.html from {app.static_folder}")
    return send_from_directory(app.static_folder, "index.html")