from flask import Flask
from controller.HomeController import home_blueprint

def create_app():
    app = Flask(__name__)

    # Register blueprints
    app.register_blueprint(home_blueprint)

    return app
