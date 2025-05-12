"""Flask application factory and server entry point."""
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv

from routes.tasks import tasks_bp
from routes.plan import plan_bp
from routes.achievements import achievements_bp


def create_app() -> Flask:
    """Create and configure Flask app."""
    load_dotenv()
    app = Flask(__name__)

    # Allow requests from any origin (adjust in production)
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # Register blueprints
    app.register_blueprint(tasks_bp, url_prefix="/api/tasks")
    app.register_blueprint(plan_bp, url_prefix="/api")
    app.register_blueprint(achievements_bp, url_prefix="/api/achievements")

    return app


if __name__ == "__main__":
    create_app().run(debug=True, host="0.0.0.0", port=8000)
