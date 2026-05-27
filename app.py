# student-api — Flask + MySQL CRUD (Activity-06)
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# local MySQL — change db name if needed
app.config["SQLALCHEMY_DATABASE_URI"] = (
    "mysql+pymysql://root:root123@localhost/student_db"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

print("Student API starting...")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5000)
