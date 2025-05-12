# app/models/user.py

from sqlalchemy import Column, String, Integer, Text, func, DateTime
from app.db.base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(64), nullable=False)
    email = Column(String(64), unique=True, index=True, nullable=False)
    photo = Column(Text, nullable=True)
    fcm = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
