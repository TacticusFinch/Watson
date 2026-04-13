import sqlite3

def create_fact_database():
    conn = sqlite3.connect("facts.db")
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS facts(id INTEGER PRIMARY KEY AUTOINCREMENT, fact TEXT NOT NULL)""")
    conn.commit()
    conn.close()

create_fact_database()

def insert_facts_from_list(facts):
    conn = sqlite3.connect("facts.db")
    cursor = conn.cursor()
    cursor.executemany("""INSERT INTO facts(fact) VALUES (?)""", [(fact,) for fact in facts])
    conn.commit()
    conn.close()
