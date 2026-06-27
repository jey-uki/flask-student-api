from flask import jsonify, request, send_file

from app.export_utils import build_export_file, parse_csv_upload
from app.extensions import db
from app.models.course_model import Course

COURSE_EXPORT_HEADERS = [
    "id",
    "course_title",
    "course_fee",
    "duration_months",
    "description",
    "is_available",
    "created_at",
]
COURSE_IMPORT_HEADERS = [
    "course_title",
    "course_fee",
    "duration_months",
    "description",
    "is_available",
]


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


def _parse_bool(value, default=True):
    if value is None or str(value).strip() == "":
        return default
    return str(value).strip().lower() in ("1", "true", "yes", "y")


def export_courses():
    format_type = request.args.get("format", "csv")
    courses = Course.query.order_by(Course.id).all()
    rows = [
        {
            "id": c.id,
            "course_title": c.course_title,
            "course_fee": c.course_fee,
            "duration_months": c.duration_months,
            "description": c.description or "",
            "is_available": c.is_available,
            "created_at": c.created_at.isoformat() if c.created_at else "",
        }
        for c in courses
    ]
    try:
        buffer, filename, mimetype = build_export_file(
            format_type,
            "Course Directory",
            COURSE_EXPORT_HEADERS,
            rows,
            "courses",
        )
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400

    return send_file(buffer, mimetype=mimetype, as_attachment=True, download_name=filename)


def import_courses():
    if "file" not in request.files:
        return jsonify({"error": "CSV file is required. Use form field 'file'."}), 400

    file_storage = request.files["file"]
    if not file_storage.filename:
        return jsonify({"error": "No file selected."}), 400
    if not file_storage.filename.lower().endswith(".csv"):
        return jsonify({"error": "Only CSV files are supported."}), 400

    rows, parse_error = parse_csv_upload(file_storage)
    if parse_error:
        return jsonify({"error": parse_error}), 400

    created = 0
    skipped = 0
    row_errors = []

    for row in rows:
        row_num = row.get("_row")
        payload = {key: row.get(key) for key in COURSE_IMPORT_HEADERS}

        errors = _validate_course_payload(payload)
        if errors:
            row_errors.append({"row": row_num, "errors": errors})
            skipped += 1
            continue

        try:
            with db.session.begin_nested():
                course = Course(
                    course_title=str(payload.get("course_title")).strip(),
                    course_fee=float(payload.get("course_fee")),
                    duration_months=int(payload.get("duration_months")),
                    description=payload.get("description") or None,
                    is_available=_parse_bool(payload.get("is_available"), default=True),
                )
                db.session.add(course)
                db.session.flush()
            created += 1
        except Exception:
            row_errors.append({"row": row_num, "errors": ["Failed to save row (duplicate title or invalid data)."]})
            skipped += 1

    try:
        db.session.commit()
    except Exception:
        db.session.rollback()
        return jsonify({"error": "An internal server error occurred during import."}), 500

    return jsonify(
        {
            "message": f"Import completed. {created} created, {skipped} skipped.",
            "created": created,
            "skipped": skipped,
            "errors": row_errors,
        }
    ), 200
