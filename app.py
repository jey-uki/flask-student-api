# student-api — Flask + MySQL CRUD (Activity-06)
from flask import Flask

app = Flask(__name__)

print("Student API starting...")

if __name__ == "__main__":
    app.run(debug=True, port=5000)
