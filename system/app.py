from flask import Flask, render_template, request, redirect, session, url_for
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'
DB_NAME = 'site.db'

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL UNIQUE,
                    password TEXT NOT NULL,
                    role TEXT NOT NULL
                )''')
    c.execute('''CREATE TABLE IF NOT EXISTS profiles (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    mobile TEXT,
                    age INTEGER,
                    gender TEXT
                )''')
    c.execute('''CREATE TABLE IF NOT EXISTS student_profiles (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    student_id INTEGER,
                    profile_id INTEGER
                )''')
    conn.commit()
    conn.close()

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username=? AND password=? AND role=?", (username, password, role))
        user = c.fetchone()
        conn.close()
        if user:
            session['user_id'] = user[0]
            session['role'] = user[3]
            return redirect(url_for('home'))
        return "Invalid credentials"
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        try:
            c.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", (username, password, role))
            conn.commit()
            conn.close()
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            conn.close()
            return "Username already exists. Try another one."
    return render_template('signup.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/home')
def home():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM profiles")
    profiles = c.fetchall()
    student_profiles = []

    if session.get('role') == 'student':
        c.execute("SELECT profile_id FROM student_profiles WHERE student_id=?", (session['user_id'],))
        student_profiles = [row[0] for row in c.fetchall()]

    conn.close()
    return render_template('home.html', profiles=profiles, role=session.get('role'), student_profiles=student_profiles)

@app.route('/add_profile', methods=['POST'])
def add_profile():
    if session.get('role') != 'recruiter':
        return redirect(url_for('home'))

    name = request.form['name']
    mobile = request.form['mobile']
    age = request.form['age']
    gender = request.form['gender']

    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO profiles (name, mobile, age, gender) VALUES (?, ?, ?, ?)", (name, mobile, age, gender))
    conn.commit()
    conn.close()

    return redirect(url_for('home'))

@app.route('/add_to_profile/<int:profile_id>')
def add_to_profile(profile_id):
    if session.get('role') != 'student':
        return redirect(url_for('home'))

    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM student_profiles WHERE student_id=? AND profile_id=?", (session['user_id'], profile_id))
    existing = c.fetchone()
    if not existing:
        c.execute("INSERT INTO student_profiles (student_id, profile_id) VALUES (?, ?)", (session['user_id'], profile_id))
        conn.commit()
    conn.close()

    return redirect(url_for('home'))

if __name__ == '__main__':
    if not os.path.exists(DB_NAME):
        init_db()
    app.run(debug=True)
