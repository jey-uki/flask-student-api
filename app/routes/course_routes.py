from flask import Blueprint
from app.middleware import roles_required

from app.controllers import course_controller as ctrl

course_bp = Blueprint("courses", __name__, url_prefix="/api/courses")


@course_bp.route("", methods=["POST"])
@roles_required("admin", "lecturer")
def create_course():
    return ctrl.create_course()


@course_bp.route("", methods=["GET"])
@roles_required("admin", "student", "lecturer")
def get_courses():
    return ctrl.get_courses()


@course_bp.route("/<int:course_id>", methods=["GET"])
@roles_required("admin", "student", "lecturer")
def get_course(course_id):
    return ctrl.get_course(course_id)


@course_bp.route("/<int:course_id>", methods=["PUT"])
@roles_required("admin", "lecturer")
def update_course(course_id):
    return ctrl.update_course(course_id)


@course_bp.route("/<int:course_id>", methods=["DELETE"])
@roles_required("admin", "lecturer")
def delete_course(course_id):
    return ctrl.delete_course(course_id)


