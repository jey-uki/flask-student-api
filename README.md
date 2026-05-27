# Student API — Flask + MySQL CRUD

REST API built with Flask, SQLAlchemy ORM, and MySQL. Manages **Students** and **Courses** with full CRUD operations.

## Setup

```bash
# 1. Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Create a .env file in the project root
cp .env.example .env   # then fill in your credentials

# 4. Create the database in MySQL
mysql -u root -p -e "CREATE DATABASE student_db;"

# 5. Run the app (tables are created automatically on first start)
python run.py
```

## Environment Variables (`.env`)

| Variable      | Description          | Default     |
|---------------|----------------------|-------------|
| `DB_USER`     | MySQL username       | `root`      |
| `DB_PASSWORD` | MySQL password       | `root123`   |
| `DB_HOST`     | MySQL host           | `localhost` |
| `DB_NAME`     | Database name        | `student_db`|
| `FLASK_DEBUG` | Enable debug mode    | `True`      |

## API Endpoints

### Students — `/api/students`

| Method | URL                    | Description         |
|--------|------------------------|---------------------|
| POST   | `/api/students`        | Create a student    |
| GET    | `/api/students`        | Get all students    |
| GET    | `/api/students/<id>`   | Get one student     |
| PUT    | `/api/students/<id>`   | Update a student    |
| DELETE | `/api/students/<id>`   | Delete a student    |

### Courses — `/api/courses`

| Method | URL                   | Description        |
|--------|-----------------------|--------------------|
| POST   | `/api/courses`        | Create a course    |
| GET    | `/api/courses`        | Get all courses    |
| GET    | `/api/courses/<id>`   | Get one course     |
| PUT    | `/api/courses/<id>`   | Update a course    |
| DELETE | `/api/courses/<id>`   | Delete a course    |

## Project Structure

```
project/
├── .env                        # local DB credentials (not committed)
├── .gitignore
├── README.md
├── requirements.txt
├── run.py                      # entry point — starts the server
└── app/
    ├── __init__.py             # create_app() factory
    ├── config.py               # loads DB config from .env
    ├── extensions.py           # SQLAlchemy db instance
    ├── utils.py                # shared helpers (utc_now, etc.)
    ├── models/
    │   ├── student_model.py
    │   └── course_model.py
    ├── controllers/
    │   ├── student_controller.py
    │   └── course_controller.py
    └── routes/
        ├── student_routes.py
        └── course_routes.py
```
