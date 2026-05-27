from flask import Flask

from app.config import Config
from app.extensions import db
from app.routes import register_blueprints


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)

    from app.models import Course, Student  # noqa: F401

    register_blueprints(app)

    return app
