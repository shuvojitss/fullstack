import sqlite3 

db = sqlite3.connect('users.db')
u = db.execute('SELECT * FROM users')
rows = u.fetchall()

for row in rows:
    print(row)

db.close()




