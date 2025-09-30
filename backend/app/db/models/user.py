from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    role = Column(String)  # student / mentor / recruiter
    tags = Column(String)  # comma separated for MVP
    points = Column(Integer, default=0)
    badges = Column(String, default="")  # comma separated

class Badge(Base):
    __tablename__ = "badges"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    description = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))

class Progress(Base):
    __tablename__ = "progress"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    quizzes_completed = Column(Integer, default=0)
    mock_interviews = Column(Integer, default=0)
    points = Column(Integer, default=0)
