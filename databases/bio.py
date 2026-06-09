from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# Настройка базы данных
Base = declarative_base()
engine = create_engine("sqlite:///bot_database.db")  # SQLite, можно заменить на PostgreSQL
Session = sessionmaker(bind=engine)
session = Session()

# Таблица пользователей
class User(Base):
    __tablename__ = "users"  # Исправлено с "tablename" на "__tablename__"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, unique=True, nullable=False)
    chat_id = Column(Integer, nullable=False)
    username = Column(String)
    full_name = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

# Таблица ответов
class Answer(Base):
    __tablename__ = "answers"  # Исправлено с "tablename" на "__tablename__"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    question_id = Column(Integer, nullable=False)
    answer = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

# Создание таблиц (должно вызываться один раз при старте приложения)
def initialize_database():
    Base.metadata.create_all(engine)