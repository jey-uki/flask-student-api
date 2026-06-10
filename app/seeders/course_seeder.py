from app import create_app
from app.extensions import db
from app.models import Course


def seed_courses():
    app = create_app()
    with app.app_context():
        if Course.query.first():
            print("Courses already exist — skipping course seeder.")
            return

        courses = [
            Course(course_title="Intro to Python", course_fee=199.0, duration_months=3, description="Beginner course covering Python basics.", is_available=True),
            Course(course_title="Web Development with Flask", course_fee=299.0, duration_months=4, description="Build web apps using Flask and SQLAlchemy.", is_available=True),
            Course(course_title="Data Structures", course_fee=249.0, duration_months=4, description="Core data structures and algorithms.", is_available=True),
            Course(course_title="Databases 101", course_fee=179.0, duration_months=2, description="Relational databases and SQL fundamentals.", is_available=True),
            Course(course_title="Machine Learning Basics", course_fee=399.0, duration_months=6, description="Introductory ML concepts and hands-on exercises.", is_available=True),
            Course(course_title="Frontend Fundamentals", course_fee=219.0, duration_months=3, description="HTML, CSS, and basic JavaScript.", is_available=True),
            Course(course_title="APIs and Microservices", course_fee=259.0, duration_months=3, description="Designing and building RESTful APIs.", is_available=True),
            Course(course_title="Cloud Essentials", course_fee=189.0, duration_months=2, description="Intro to cloud providers and deployment.", is_available=True),
            Course(course_title="DevOps Fundamentals", course_fee=279.0, duration_months=3, description="CI/CD, containers, and infrastructure as code.", is_available=True),
            Course(course_title="Advanced Python", course_fee=329.0, duration_months=4, description="Advanced Python patterns and tooling.", is_available=True),
        ]

        db.session.bulk_save_objects(courses)
        db.session.commit()
        print(f"Inserted {len(courses)} courses.")


if __name__ == "__main__":
    seed_courses()
