from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Initialize DB
def init_db():
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        mobile TEXT,
        email TEXT,
        summary TEXT,
        address TEXT
    )''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute("SELECT id, name, mobile FROM users")
    users = c.fetchall()
    conn.close()
    return render_template('index.html', users=users)

@app.route('/add', methods=['POST'])
def add():
    name = request.form['name']
    mobile = request.form['mobile']
    email = request.form['email']
    summary = request.form['summary']
    address = request.form['address']

    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute("INSERT INTO users (name, mobile, email, summary, address) VALUES (?, ?, ?, ?, ?)",
              (name, mobile, email, summary, address))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/detail/<int:user_id>')
def detail(user_id):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user = c.fetchone()
    conn.close()
    return render_template('detail.html', user=user)

@app.route('/delete/<int:user_id>', methods=['POST'])
def delete(user_id):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute("DELETE FROM users WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
