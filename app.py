# student-api — Flask + MySQL CRUD (Activity-06)
from datetime import datetime, date

from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import OperationalError, ProgrammingError

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = (
    "mysql+pymysql://root:root123@localhost/student_db"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class Student(db.Model):
    __tablename__ = "students"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    age = db.Column(db.Integer, nullable=False)
    cgpa = db.Column(db.Float, default=0.0)
    is_active = db.Column(db.Boolean, default=True)
    joined_date = db.Column(db.Date, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "full_name": self.full_name,
            "email": self.email,
            "age": self.age,
            "cgpa": self.cgpa,
            "is_active": self.is_active,
            "joined_date": self.joined_date.isoformat() if self.joined_date else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }


class Course(db.Model):
    __tablename__ = "courses"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    course_title = db.Column(db.String(100), nullable=False, unique=True)
    course_fee = db.Column(db.Float, nullable=False)
    duration_months = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text, nullable=True)
    is_available = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "course_title": self.course_title,
            "course_fee": self.course_fee,
            "duration_months": self.duration_months,
            "description": self.description,
            "is_available": self.is_available,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }


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
    elif email is not None and str(email).strip():
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


@app.route("/api/students", methods=["POST"])
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
        age_val = int(data.get("age"))
        student = Student(
            full_name=data.get("full_name").strip(),
            email=data.get("email").strip(),
            age=age_val,
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


print("Student API starting...")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5000)
