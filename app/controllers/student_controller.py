from datetime import datetime

from flask import jsonify, request, send_file

from app.export_utils import build_export_file, parse_csv_upload
from app.extensions import db
from app.models.student_model import Student

STUDENT_EXPORT_HEADERS = [
    "id",
    "full_name",
    "email",
    "age",
    "cgpa",
    "is_active",
    "joined_date",
    "created_at",
]
STUDENT_IMPORT_HEADERS = ["full_name", "email", "age", "cgpa", "is_active", "joined_date"]


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


def _parse_bool(value, default=True):
    if value is None or str(value).strip() == "":
        return default
    return str(value).strip().lower() in ("1", "true", "yes", "y")


def export_students():
    format_type = request.args.get("format", "csv")
    students = Student.query.order_by(Student.id).all()
    rows = [
        {
            "id": s.id,
            "full_name": s.full_name,
            "email": s.email,
            "age": s.age,
            "cgpa": s.cgpa,
            "is_active": s.is_active,
            "joined_date": s.joined_date.isoformat() if s.joined_date else "",
            "created_at": s.created_at.isoformat() if s.created_at else "",
        }
        for s in students
    ]
    try:
        buffer, filename, mimetype = build_export_file(
            format_type,
            "Student Directory",
            STUDENT_EXPORT_HEADERS,
            rows,
            "students",
        )
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400

    return send_file(buffer, mimetype=mimetype, as_attachment=True, download_name=filename)


def import_students():
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
        payload = {key: row.get(key) for key in STUDENT_IMPORT_HEADERS}

        errors = _validate_student_payload(payload)
        if errors:
            row_errors.append({"row": row_num, "errors": errors})
            skipped += 1
            continue

        joined_date, date_err = _parse_joined_date(payload.get("joined_date"))
        if date_err:
            row_errors.append({"row": row_num, "errors": [date_err]})
            skipped += 1
            continue

        try:
            with db.session.begin_nested():
                student = Student(
                    full_name=str(payload.get("full_name")).strip(),
                    email=str(payload.get("email")).strip(),
                    age=int(payload.get("age")),
                    cgpa=float(payload.get("cgpa") or 0.0),
                    is_active=_parse_bool(payload.get("is_active"), default=True),
                    joined_date=joined_date,
                )
                db.session.add(student)
                db.session.flush()
            created += 1
        except Exception:
            row_errors.append({"row": row_num, "errors": ["Failed to save row (duplicate email or invalid data)."]})
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
