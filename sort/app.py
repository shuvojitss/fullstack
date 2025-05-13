from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

def get_students(order='ASC'):
    conn = sqlite3.connect('students.db')
    c = conn.cursor()
    c.execute(f"SELECT name, guardian_salary FROM students ORDER BY guardian_salary {order}")
    students = c.fetchall()
    conn.close()
    return students

@app.route("/", methods=["GET", "POST"])
def index():
    order = request.form.get("sort_order", "ASC")
    students = get_students(order)
    return render_template("index.html", students=students, current_order=order)

if __name__ == "__main__":
    app.run(debug=True)
