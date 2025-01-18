import sqlite3
import json

from handlers.user_private import might_questions


def create_database():
    conn = sqlite3.connect("might_questions.db")
    cursor = conn.cursor()
    cursor.execute(("CREATE TABLE IF NOT EXISTS questions(id INTEGER PRIMARY KEY AUTOINCREMENT, question TEXT NOT NULL, image_path TEXT, options TEXT NOT NULL, correct INTEGER NOT NULL)"))
    conn.commit()
    conn.close()
def insert_questions(might_questions):
    conn = sqlite3.connect('might_questions.db')
    cursor = conn.cursor()
    # Итерация по списку вопросов
    for question_data in might_questions:
        options_json = json.dumps(question_data["options"])
        cursor.execute(
            "INSERT INTO questions (question, image_path, options, correct) VALUES (?, ?, ?, ?)",
            (question_data['question'], question_data.get('image_path'), options_json, question_data['correct'])
        )
    conn.commit()
    conn.close()
