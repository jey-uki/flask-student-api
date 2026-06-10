"""Run all seeders."""

from app.seeders.student_seeder import seed_students
from app.seeders.course_seeder import seed_courses


def run_all():
    print("Running course seeder...")
    seed_courses()
    print("Running student seeder...")
    seed_students()


if __name__ == "__main__":
    run_all()
