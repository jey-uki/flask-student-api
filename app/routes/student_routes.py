from flask import Blueprint
from app.middleware import roles_required

from app.controllers import student_controller as ctrl

student_bp = Blueprint("students", __name__, url_prefix="/api/students")


@student_bp.route("", methods=["POST"])
@roles_required("admin")
def create_student():
    return ctrl.create_student()


@student_bp.route("", methods=["GET"])
@roles_required("admin", "lecturer")
def get_students():
    return ctrl.get_students()


@student_bp.route("/<int:student_id>", methods=["GET"])
@roles_required("admin", "student", "lecturer")
def get_student(student_id):
    return ctrl.get_student(student_id)


@student_bp.route("/<int:student_id>", methods=["PUT"])
@roles_required("student")
def update_student(student_id):
    return ctrl.update_student(student_id)


@student_bp.route("/<int:student_id>", methods=["DELETE"])
@roles_required("admin")
def delete_student(student_id):
    return ctrl.delete_student(student_id)


