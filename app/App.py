from flask import Flask, jsonify, send_file, send_from_directory, request
import os
from werkzeug.exceptions import HTTPException
from config.config import Config
from extensions.db import db
from extensions.bcrypt import bcrypt
from extensions.jwt import jwt

# Blueprints
from controller.AuthController import auth_bp
from controller.UserController import user_bp
from controller.TaskController import task_bp
from controller.HomeController import home_blueprint
from controller.StatusController import status_bp
from controller.PriorityController import priority_bp

# Seeds
from seed.seed_users import seed_users
from seed.seed_priority import seed_priority
from seed.seed_status import seed_status


def create_app():
    # Load config first to get static folder and url path
    config = Config
    app = Flask(
        __name__,
        static_folder=config.STATIC_FOLDER,
        static_url_path=config.STATIC_URL_PATH
    )

    app.config.from_object(config)
    app.config["PROPAGATE_EXCEPTIONS"] = False

    # Extensions
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    # Register API blueprints FIRST
    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(task_bp)
    app.register_blueprint(status_bp)
    app.register_blueprint(priority_bp)

    # Register HomeController LAST (important for SPA routing)
    app.register_blueprint(home_blueprint)

    # Health check
    @app.get("/health")
    def health():
        return {"status": "Server is running"}

    # API docs
    @app.get("/api/docs")
    def docs():
        doc_path = os.path.join(os.path.dirname(__file__), "api_doc.md")
        return send_file(doc_path, mimetype="text/markdown")

    # ---------------------------
    # SPA-AWARE 404 HANDLER
    # ---------------------------
    @app.errorhandler(404)
    def not_found(e):
        # API routes → return JSON
        if request.path.startswith("/api"):
            return jsonify({
                "error": "Not Found",
                "message": "The requested URL was not found.",
                "status": 404
            }), 404

        # Frontend routes → return React index.html
        return send_from_directory(app.static_folder, "index.html")

    # Generic exception handler
    @app.errorhandler(Exception)
    def handle_exception(e):
        app.logger.exception("Unhandled exception")
        return jsonify({
            "error": "Internal Server Error",
            "message": "An unexpected error occurred.",
            "status": 500,
        }), 500

    # Initialize database and seed data
    with app.app_context():
        try:
            db.create_all()
            seed_users()
            seed_priority()
            seed_status()
        except Exception as e:
            app.logger.warning(f"Database initialization skipped: {e}")
            print(f"⚠️ Database not accessible. Run 'flask init-db' manually.")

    # CLI command
    @app.cli.command()
    def init_db():
        """Initialize the database and seed initial data."""
        try:
            db.create_all()
            seed_users()
            seed_priority()
            seed_status()
            print("✓ Database initialized successfully!")
        except Exception as e:
            print(f"✗ Error initializing database: {e}")

    return app


app = create_app()
