# app/models/match.py
from sqlalchemy import Column, Integer, String, Float, ForeignKey, UUID
from sqlalchemy.orm import relationship

from app.db.base import Base

class Match(Base):
    __tablename__ = "matches"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    source_case_id = Column(String(36), ForeignKey("cases.id"), nullable=False)
    matched_case_id = Column(String(36), ForeignKey("cases.id"), nullable=False)
    similarity = Column(Float, nullable=False)

    # Optional relationships (useful if you want to access case details directly)
    source_case = relationship("Case", foreign_keys=[source_case_id], backref="matches_from")
    matched_case = relationship("Case", foreign_keys=[matched_case_id], backref="matches_to")
