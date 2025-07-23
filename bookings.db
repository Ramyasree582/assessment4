import sqlite3

conn = sqlite3.connect('bookings.db')
c = conn.cursor()

c.execute('''
    CREATE TABLE IF NOT EXISTS bookings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        phone TEXT,
        movie TEXT,
        theater TEXT,
        timing TEXT,
        date TEXT,
        persons INTEGER,
        seats TEXT
    )
''')

conn.commit()
conn.close()

print("Database initialized.")
