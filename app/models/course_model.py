from app.extensions import db
from app.utils import utc_now


class Course(db.Model):
    __tablename__ = "courses"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    course_title = db.Column(db.String(100), nullable=False, unique=True)
    course_fee = db.Column(db.Float, nullable=False)
    duration_months = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text, nullable=True)
    is_available = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=utc_now)

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
