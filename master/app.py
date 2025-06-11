from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'
with sqlite3.connect('users.db') as conn:
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS entries (id INTEGER PRIMARY KEY, name TEXT, email TEXT, salary INTEGER)''')
    c.execute('''CREATE TABLE IF NOT EXISTS favorites (id INTEGER PRIMARY KEY, user TEXT, entry_id INTEGER)''')
    conn.commit()

@app.route('/')
def index():
    return redirect('/login')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        with sqlite3.connect('users.db') as conn:
            conn.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
        return redirect('/login')
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        with sqlite3.connect('users.db') as conn:
            user = conn.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password)).fetchone()
        if user:
            session['username'] = username
            return redirect('/home')
        else:
            return "Invalid credentials"
    return render_template('login.html')

@app.route('/home')
def home():
    if 'username' not in session:
        return redirect('/login')
    with sqlite3.connect('users.db') as conn:
        entries = conn.execute("SELECT * FROM entries").fetchall()
        fav_ids = [row[0] for row in conn.execute("SELECT entry_id FROM favorites WHERE user=?", (session['username'],)).fetchall()]
    return render_template('home.html', entries=entries, fav_ids=fav_ids, filter=False)

@app.route('/favorite/<int:entry_id>')
def favorite(entry_id):
    if 'username' in session:
        with sqlite3.connect('users.db') as conn:
            conn.execute("INSERT INTO favorites (user, entry_id) VALUES (?, ?)", (session['username'], entry_id))
            conn.commit()
    return redirect('/home')

@app.route('/profile')
def profile():
    if 'username' not in session:
        return redirect('/login')
    with sqlite3.connect('users.db') as conn:
        favs = conn.execute("SELECT e.* FROM entries e JOIN favorites f ON e.id = f.entry_id WHERE f.user=?", (session['username'],)).fetchall()
    return render_template('home.html', entries=favs, fav_ids=[e[0] for e in favs], filter=True)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/login')

if __name__ == '__main__':
    app.run(debug=True)
