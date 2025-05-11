import sqlite3


conn = sqlite3.connect('HomeQuest.db')
c = conn.cursor()

c.execute('''
    CREATE TABLE IF NOT EXISTS contacts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        mail TEXT NOT NULL,
        question TEXT NOT NULL
    )
''')


conn.commit()
conn.close()
