import sqlite3

conn = sqlite3.connect("students.db")
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    guardian_salary INTEGER NOT NULL
)''')

students = [
    ("Alice", 30000),
    ("Bob", 45000),
    ("Charlie", 25000),
    ("Diana", 50000),
    ("Evan", 40000),
    ("Fiona", 20000),
    ("George", 35000),
    ("Hannah", 28000),
    ("Ian", 60000),
    ("Julia", 22000)
]

c.executemany("INSERT INTO students (name, guardian_salary) VALUES (?, ?)", students)
conn.commit()
conn.close()
