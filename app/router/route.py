from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, Form, File, UploadFile
from sqlalchemy.orm import Session

from app.controller.case import create_case
from app.core.security import get_current_user
from app.crud.case import crud_get_cases
from app.crud.match import crud_get_matches
from app.schemas.auth import AuthResponse, AuthRequest
from app.controller.auth import authenticate_user
from app.db.session import SessionLocal
from app.schemas.case import CaseResponse

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/auth", response_model=AuthResponse)
async def auth(body: AuthRequest, db: Session = Depends(get_db)):
    return authenticate_user(body.token, body.fcm, db)

@router.get("/case", response_model=List[CaseResponse])
async def case_fetch(current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    return crud_get_cases(db, current_user)

@router.post("/case", response_model=CaseResponse)
async def case_create(
    name: str = Form(...),
    phone: str = Form(...),
    address: str = Form(...),
    case_type: str = Form(...),
    photo: UploadFile = File(...),
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return await create_case(current_user, name=name, phone=phone, photo=photo, address=address, case_type=case_type, db=db)

@router.get("/match/{case_id}")
async def case_fetch_matches(case_id: str,current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    matches = await crud_get_matches(db, case_id)
    response = []
    for match in matches:
        response.append({
            "matched_id": match.matched_id,
            "matched_name": match.matched_name,
            "similarity": match.similarity,
            "source_photo": match.source_photo,
            "matched_photo": match.matched_photo,
            "matched_phone": match.matched_phone,
            "matched_address": match.matched_address
        })
    return response