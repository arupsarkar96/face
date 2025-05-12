# app/schemas/match.py
from pydantic import BaseModel

class MatchCreate(BaseModel):
    source_case_id: str
    matched_case_id: str
    similarity: float

class MatchResponse(MatchCreate):
    id: str

    class Config:
        from_attributes = True
