from flask import Flask, send_file
import os
from config.config import Config
from extensions.db import db
from extensions.bcrypt import bcrypt
from extensions.jwt import jwt
from controller.AuthController import auth_bp
from controller.UserController import user_bp
from controller.TaskController import task_bp
from seed.seed_users import seed_users
from seed.seed_priority import seed_priority
from seed.seed_status import seed_status


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(task_bp)

    @app.get("/")
    def health():
        return {"status": "Server is running"}

    @app.get("/api/docs")
    def docs():
        doc_path = os.path.join(os.path.dirname(__file__), "api_doc.md")
        return send_file(doc_path, mimetype="text/markdown")

    # Initialize database and seed data (only in development or if db is accessible)
    with app.app_context():
        try:
            db.create_all()
            seed_users()
            seed_priority()
            seed_status()
        except Exception as e:
            app.logger.warning(f"Database initialization skipped: {e}")
            print(f"⚠️  Database not accessible. Run 'flask init-db' to initialize.")

    # Register CLI command for manual database initialization
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
