from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

def get_users(name=None, mobile=None, age=None):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    
    query = "SELECT * FROM users WHERE 1=1"
    params = []

    if name:
        query += " AND name LIKE ?"
        params.append(f"%{name}%")
    if mobile:
        query += " AND mobile LIKE ?"
        params.append(f"%{mobile}%")
    if age:
        query += " AND age = ?"
        params.append(age)

    cursor.execute(query, params)
    users = cursor.fetchall()
    conn.close()
    return users

@app.route("/", methods=["GET", "POST"])
def index():
    name = request.form.get("name")
    mobile = request.form.get("mobile")
    age = request.form.get("age")
    
    users = get_users(name, mobile, age)
    return render_template("index.html", users=users)

if __name__ == "__main__":
    app.run(debug=True)
