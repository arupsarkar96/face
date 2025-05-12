# app/models/case.py

from sqlalchemy import Column, Enum as SQLAlchemyEnum, String, Boolean, JSON, null, DateTime, func
from app.db.base import Base
import uuid
import enum

# Define the Python Enum
class CaseType(str, enum.Enum):
    LOST = "LOST"
    FOUND = "FOUND"

class Case(Base):
    __tablename__ = "cases"

    id = Column(String(36), primary_key=True)
    user_id = Column(String(64), index=True)  # You can make this a ForeignKey if needed
    name = Column(String(64), nullable=False)
    phone = Column(String(10), nullable=False)
    photo = Column(String(255), nullable=True)
    address = Column(String(255), nullable=True)
    type = Column(SQLAlchemyEnum(CaseType), nullable=False)
    is_closed = Column(Boolean, default=False)
    data = Column(JSON, nullable=True, default=null)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
