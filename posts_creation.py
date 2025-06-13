import sqlite3

conn = sqlite3.connect('HomeQuest.db')
c = conn.cursor()

conn.execute('''
            CREATE TABLE IF NOT EXISTS posts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT NOT NULL,
                publisher TEXT NOT NULL,
                picture_url TEXT NOT NULL,
                price TEXT NOT NULL,
                section TEXT NOT NULL
            )
        ''')

conn.close()