# database/models.py
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from database.db import Base
import datetime

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    tg_id = Column(Integer, unique=True, index=True)
    name = Column(String, nullable=False)
    age = Column(String)
    level = Column(String)
    goal_time = Column(String)
    tutor_importance = Column(String)
    strong_sides = Column(String)
    weekly_lessons = Column(String)
    format = Column(String)
    topics = Column(String)
    schedule = Column(String)
    vpn = Column(String)
    wishes = Column(String)

class LessonSlot(Base):
    __tablename__ = "lesson_slots"
    id = Column(Integer, primary_key=True)
    datetime_str = Column(String, unique=True)
    booked_by = Column(Integer, ForeignKey("users.tg_id"), nullable=True)

class Question(Base):
    __tablename__ = "questions"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    text = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class Homework(Base):
    __tablename__ = "homework"
    id = Column(Integer, primary_key=True)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class Payment(Base):
    __tablename__ = "payments"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    filename = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
