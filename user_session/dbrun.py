import sqlite3
import os
conn = sqlite3.connect('users.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS entries (id INTEGER PRIMARY KEY, name TEXT, email TEXT, salary INTEGER)''')
c.execute("SELECT COUNT(*) FROM entries")
if c.fetchone()[0] == 0:
    c.executemany("INSERT INTO entries (name, email, salary) VALUES (?, ?, ?)", [
        ('Alice', 'alice@example.com', 50000),
        ('Bob', 'bob@example.com', 60000),
        ('Charlie', 'charlie@example.com', 70000),
        ('David', 'david@example.com', 75000),
        ('Eva', 'eva@example.com', 80000),
        ('Frank', 'frank@example.com', 85000),
        ('Grace', 'grace@example.com', 90000),
        ('Hannah', 'hannah@example.com', 95000),
        ('Ivy', 'ivy@example.com', 100000),
        ('Jack', 'jack@example.com', 105000)
    ])
    conn.commit()

conn.close()
