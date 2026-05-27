from flask import jsonify, request

from app.extensions import db
from app.models.course_model import Course


def _validate_course_payload(data, course_id=None):
    errors = []
    if not data:
        return ["Request body is required."]

    title = data.get("course_title")
    if title is None or str(title).strip() == "":
        errors.append("course_title is required.")
    elif str(title).strip():
        q = Course.query.filter(Course.course_title == str(title).strip())
        if course_id:
            q = q.filter(Course.id != course_id)
        if q.first():
            errors.append("Course title already exists.")

    fee = data.get("course_fee")
    if fee is None:
        errors.append("course_fee is required.")
    else:
        try:
            fee_val = float(fee)
            if fee_val <= 0:
                errors.append("course_fee must be a positive number.")
        except (TypeError, ValueError):
            errors.append("course_fee must be a positive number.")

    duration = data.get("duration_months")
    if duration is None:
        errors.append("duration_months is required.")
    else:
        try:
            dur_val = int(duration)
            if dur_val <= 0:
                errors.append("duration_months must be a positive integer.")
        except (TypeError, ValueError):
            errors.append("duration_months must be a positive integer.")

    return errors


def create_course():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Request body is required."}), 400

    errors = _validate_course_payload(data)
    if errors:
        return jsonify({"errors": errors}), 400

    try:
        course = Course(
            course_title=data.get("course_title").strip(),
            course_fee=float(data.get("course_fee")),
            duration_months=int(data.get("duration_months")),
            description=data.get("description"),
            is_available=data.get("is_available", True),
        )
        db.session.add(course)
        db.session.commit()
        return jsonify({"message": "Course created successfully.", "course": course.to_dict()}), 201
    except Exception:
        db.session.rollback()
        return jsonify({"error": "An internal server error occurred."}), 500


def get_courses():
    courses = Course.query.all()
    return jsonify({"courses": [c.to_dict() for c in courses]}), 200


def get_course(course_id):
    course = Course.query.get(course_id)
    if not course:
        return jsonify({"error": "Course not found."}), 404
    return jsonify({"course": course.to_dict()}), 200


def update_course(course_id):
    course = Course.query.get(course_id)
    if not course:
        return jsonify({"error": "Course not found."}), 404

    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "No data provided to update."}), 400

    errors = _validate_course_payload(data, course_id=course_id)
    if errors:
        return jsonify({"errors": errors}), 400

    try:
        course.course_title = data.get("course_title").strip()
        course.course_fee = float(data.get("course_fee"))
        course.duration_months = int(data.get("duration_months"))
        if "description" in data:
            course.description = data.get("description")
        if "is_available" in data:
            course.is_available = bool(data.get("is_available"))
        db.session.commit()
        return jsonify({"message": "Course updated successfully.", "course": course.to_dict()}), 200
    except Exception:
        db.session.rollback()
        return jsonify({"error": "An internal server error occurred."}), 500


def delete_course(course_id):
    course = Course.query.get(course_id)
    if not course:
        return jsonify({"error": "Course not found."}), 404
    try:
        db.session.delete(course)
        db.session.commit()
        return jsonify({"message": "Course deleted successfully."}), 200
    except Exception:
        db.session.rollback()
        return jsonify({"error": "An internal server error occurred."}), 500
