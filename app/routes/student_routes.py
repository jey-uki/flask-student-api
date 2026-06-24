from flask import Blueprint
from flask_jwt_extended import jwt_required

from app.controllers import student_controller as ctrl

student_bp = Blueprint("students", __name__, url_prefix="/api/students")


@student_bp.route("", methods=["POST"])
@jwt_required()
def create_student():
    return ctrl.create_student()


@student_bp.route("", methods=["GET"])
@jwt_required()
def get_students():
    return ctrl.get_students()


@student_bp.route("/<int:student_id>", methods=["GET"])
@jwt_required()
def get_student(student_id):
    return ctrl.get_student(student_id)


@student_bp.route("/<int:student_id>", methods=["PUT"])
@jwt_required()
def update_student(student_id):
    return ctrl.update_student(student_id)


@student_bp.route("/<int:student_id>", methods=["DELETE"])
@jwt_required()
def delete_student(student_id):
    return ctrl.delete_student(student_id)

