from datetime import datetime

from flask import jsonify, request

from app.extensions import db
from app.models.student_model import Student


def _parse_joined_date(value):
    if not value:
        return None, "joined_date is required."
    try:
        if isinstance(value, str):
            return datetime.strptime(value, "%Y-%m-%d").date(), None
        return value, None
    except ValueError:
        return None, "joined_date must be in YYYY-MM-DD format."


def _validate_student_payload(data, student_id=None):
    errors = []
    if not data:
        return ["Request body is required."]

    full_name = data.get("full_name")
    if full_name is None or str(full_name).strip() == "":
        errors.append("full_name is required.")

    email = data.get("email")
    if email is None or str(email).strip() == "":
        errors.append("email is required.")
    elif str(email).strip():
        q = Student.query.filter(Student.email == str(email).strip())
        if student_id:
            q = q.filter(Student.id != student_id)
        if q.first():
            errors.append("Email address already exists.")

    age = data.get("age")
    if age is None:
        errors.append("age is required.")
    else:
        try:
            age_val = int(age)
            if age_val <= 0:
                errors.append("age must be a positive integer.")
        except (TypeError, ValueError):
            errors.append("age must be a positive integer.")

    joined_raw = data.get("joined_date")
    if joined_raw is None or str(joined_raw).strip() == "":
        errors.append("joined_date is required.")

    return errors


def create_student():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Request body is required."}), 400

    errors = _validate_student_payload(data)
    if errors:
        return jsonify({"errors": errors}), 400

    joined_date, date_err = _parse_joined_date(data.get("joined_date"))
    if date_err:
        return jsonify({"error": date_err}), 400

    try:
        student = Student(
            full_name=data.get("full_name").strip(),
            email=data.get("email").strip(),
            age=int(data.get("age")),
            cgpa=float(data.get("cgpa", 0.0)),
            is_active=data.get("is_active", True),
            joined_date=joined_date,
        )
        db.session.add(student)
        db.session.commit()
        return jsonify({"message": "Student created successfully.", "student": student.to_dict()}), 201
    except Exception:
        db.session.rollback()
        return jsonify({"error": "An internal server error occurred."}), 500


def get_students():
    students = Student.query.all()
    return jsonify({"students": [s.to_dict() for s in students]}), 200


def get_student(student_id):
    student = Student.query.get(student_id)
    if not student:
        return jsonify({"error": "Student not found."}), 404
    return jsonify({"student": student.to_dict()}), 200


def update_student(student_id):
    student = Student.query.get(student_id)
    if not student:
        return jsonify({"error": "Student not found."}), 404

    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "No data provided to update."}), 400

    errors = _validate_student_payload(data, student_id=student_id)
    if errors:
        return jsonify({"errors": errors}), 400

    joined_date, date_err = _parse_joined_date(data.get("joined_date"))
    if date_err:
        return jsonify({"error": date_err}), 400

    try:
        student.full_name = data.get("full_name").strip()
        student.email = data.get("email").strip()
        student.age = int(data.get("age"))
        if "cgpa" in data:
            student.cgpa = float(data.get("cgpa"))
        if "is_active" in data:
            student.is_active = bool(data.get("is_active"))
        student.joined_date = joined_date
        db.session.commit()
        return jsonify({"message": "Student updated successfully.", "student": student.to_dict()}), 200
    except Exception:
        db.session.rollback()
        return jsonify({"error": "An internal server error occurred."}), 500


def delete_student(student_id):
    student = Student.query.get(student_id)
    if not student:
        return jsonify({"error": "Student not found."}), 404
    try:
        db.session.delete(student)
        db.session.commit()
        return jsonify({"message": "Student deleted successfully."}), 200
    except Exception:
        db.session.rollback()
        return jsonify({"error": "An internal server error occurred."}), 500
