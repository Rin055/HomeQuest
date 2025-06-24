import sqlite3

conn = sqlite3.connect('HomeQuest.db')
c = conn.cursor()
c.execute('''
    CREATE TABLE IF NOT EXISTS customers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
         name TEXT
    )
''')
conn.commit()
conn.close()
