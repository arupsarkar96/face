# app/schemas/case.py

from pydantic import BaseModel, UUID4
from enum import Enum

class CaseType(str, Enum):
    LOST = "LOST"
    FOUND = "FOUND"

class CaseResponse(BaseModel):
    id: UUID4
    user_id: str
    name: str
    phone: str
    photo: str
    type: CaseType
    is_closed: bool

    model_config = {
        "from_attributes": True
    }
