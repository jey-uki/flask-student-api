# student-api — Flask + MySQL CRUD (Activity-06)
from datetime import datetime, date

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Boolean, Date, DateTime, Float, Integer, String, Text

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = (
    "mysql+pymysql://root:root123@localhost/student_db"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class Student(db.Model):
    __tablename__ = "students"

    id = db.Column(Integer, primary_key=True, autoincrement=True)
    full_name = db.Column(String(100), nullable=False)
    email = db.Column(String(120), nullable=False, unique=True)
    age = db.Column(Integer, nullable=False)
    cgpa = db.Column(Float, default=0.0)
    is_active = db.Column(Boolean, default=True)
    joined_date = db.Column(Date, nullable=False)
    created_at = db.Column(DateTime, default=datetime.utcnow)

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


print("Student API starting...")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5000)
