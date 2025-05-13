from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

def get_students(order='ASC', search_term=''):
    conn = sqlite3.connect('students.db')
    c = conn.cursor()
    
    if search_term:
        c.execute(f"""
            SELECT name, guardian_salary 
            FROM students 
            WHERE LOWER(name) LIKE ? 
            ORDER BY guardian_salary {order}
        """, ('%' + search_term.lower() + '%',))
    else:
        c.execute(f"SELECT name, guardian_salary FROM students ORDER BY guardian_salary {order}")
    
    students = c.fetchall()
    conn.close()
    return students

@app.route("/", methods=["GET", "POST"])
def index():
    order = request.form.get("sort_order", "ASC")
    search = request.form.get("search", "").strip()
    students = get_students(order, search)
    return render_template("index.html", students=students, current_order=order, search_term=search)

if __name__ == "__main__":
    app.run(debug=True)
