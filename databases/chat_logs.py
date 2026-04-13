import sqlite3

conn = sqlite3.connect('chat_log.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS chat_messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT,
    message TEXT,
    date_time TEXT
)
''')
conn.commit()
conn.close()