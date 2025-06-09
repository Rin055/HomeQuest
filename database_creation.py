import sqlite3

conn = sqlite3.connect('HomeQuest.db')
c = conn.cursor()


conn.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                email TEXT NOT NULL,
                age INTEGER NOT NULL
            )
        ''')


try:
    conn.execute("ALTER TABLE posts ADD COLUMN short_description TEXT NOT NULL DEFAULT ''")
except sqlite3.OperationalError:
    pass

conn.execute('''
    INSERT INTO users (username, email, age) VALUES ('Mariam Koberidze', 'mary@gmail.com', 16)
''')
conn.commit()

conn.execute('''
    UPDATE users SET password = '123' WHERE email = 'mari@gmail.com'
''')
conn.commit()

conn.execute('''
    DELETE FROM users WHERE id = 1
''')
conn.commit()

c.execute('SELECT id, username FROM users')
rows = c.fetchall()
for row in rows:
    print(f"ID: {row[0]}, Username: {row[1]}")


conn.close()