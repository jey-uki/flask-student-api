from datetime import date

from app import create_app
from app.extensions import db
from app.models import Student


def seed_students():
    app = create_app()
    with app.app_context():
        if Student.query.first():
            print("Students already exist — skipping student seeder.")
            return

        students = [
            Student(full_name="Alice Smith", email="alice.smith@example.com", age=20, cgpa=3.5, is_active=True, joined_date=date(2023, 9, 1)),
            Student(full_name="Bob Johnson", email="bob.johnson@example.com", age=22, cgpa=3.7, is_active=True, joined_date=date(2022, 8, 15)),
            Student(full_name="Catherine Liu", email="catherine.liu@example.com", age=21, cgpa=3.9, is_active=True, joined_date=date(2023, 1, 10)),
            Student(full_name="Daniel Kim", email="daniel.kim@example.com", age=24, cgpa=2.8, is_active=False, joined_date=date(2021, 6, 20)),
            Student(full_name="Elena Garcia", email="elena.garcia@example.com", age=19, cgpa=3.2, is_active=True, joined_date=date(2024, 2, 5)),
            Student(full_name="Farhan Ali", email="farhan.ali@example.com", age=23, cgpa=3.0, is_active=True, joined_date=date(2022, 11, 30)),
            Student(full_name="Gabriella Rossi", email="gabriella.rossi@example.com", age=20, cgpa=3.6, is_active=True, joined_date=date(2023, 5, 17)),
            Student(full_name="Hiro Tanaka", email="hiro.tanaka@example.com", age=25, cgpa=2.9, is_active=False, joined_date=date(2020, 9, 1)),
            Student(full_name="Isha Patel", email="isha.patel@example.com", age=22, cgpa=3.4, is_active=True, joined_date=date(2021, 3, 8)),
            Student(full_name="Jonas Müller", email="jonas.muller@example.com", age=21, cgpa=3.8, is_active=True, joined_date=date(2024, 4, 1)),
        ]

        db.session.bulk_save_objects(students)
        db.session.commit()
        print(f"Inserted {len(students)} students.")


if __name__ == "__main__":
    seed_students()
