import sqlite3

conn = sqlite3.connect('HomeQuest.db')
c = conn.cursor()

c.execute('''
    CREATE TABLE IF NOT EXISTS wishlist (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_email TEXT NOT NULL,
        post_id INTEGER NOT NULL,
        UNIQUE(customer_email, post_id)
    )
''')

conn.commit()
conn.close()