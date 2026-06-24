from app.routes.auth_routes import auth_bp
from app.routes.course_routes import course_bp
from app.routes.student_routes import student_bp


def register_blueprints(app):
    app.register_blueprint(student_bp)
    app.register_blueprint(course_bp)
    app.register_blueprint(auth_bp)

