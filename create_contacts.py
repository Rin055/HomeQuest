import sqlite3

conn = sqlite3.connect('HomeQuest.db')
c = conn.cursor()

conn.execute('''
            CREATE TABLE IF NOT EXISTS contacts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                question TEXT NOT NULL
            )
        ''')

conn.close()