# student-api — Flask + MySQL CRUD (Activity-06)
from datetime import datetime, date

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
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


print("Student API starting...")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5000)
