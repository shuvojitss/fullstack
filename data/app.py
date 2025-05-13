from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Create table if not exists
def init_db():
    with sqlite3.connect("database.db") as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS employees (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            name TEXT NOT NULL,
                            mobile TEXT NOT NULL,
                            email TEXT NOT NULL,
                            salary REAL NOT NULL
                        )''')
init_db()

# Route to display page
@app.route('/')
def index():
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM employees")
    employees = cur.fetchall()
    conn.close()
    return render_template("index.html", employees=employees)

# Route to handle form submission
@app.route('/add', methods=["POST"])
def add():
    name = request.form['name']
    mobile = request.form['mobile']
    email = request.form['email']
    salary = request.form['salary']

    with sqlite3.connect("database.db") as conn:
        conn.execute("INSERT INTO employees (name, mobile, email, salary) VALUES (?, ?, ?, ?)",
                     (name, mobile, email, salary))
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
