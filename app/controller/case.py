import os
import uuid
from fastapi import UploadFile
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse
from app.crud.case import crud_create_case
from app.models.case import Case
from app.services.celery import start_matching
from app.utils.face import get_embedding

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

async def create_case(user: str, name: str, phone: str, photo: UploadFile, address: str, case_type: str, db: Session):
    allowed_extensions = {"jpg", "jpeg", "png", "webp"}
    ext = photo.filename.rsplit(".", 1)[-1].lower()

    if ext not in allowed_extensions:
        return JSONResponse(status_code=400, content={"error": "Unsupported file format"})

    # Generate safe file ID and path
    case_id = uuid.uuid4()
    file_id = str(case_id)
    filename = f"{file_id}.{ext}"
    file_path = os.path.join(UPLOAD_DIR, filename)


    # Save file
    with open(file_path, "wb") as f:
        f.write(await photo.read())

    embedding = get_embedding(file_path)

    create = Case(
        id = str(case_id),
        user_id = user,
        name = name,
        phone = phone,
        address = address,
        photo = filename,
        type = case_type,
        data = embedding.astype(float).tolist()
    )
    case = crud_create_case(db, case=create)
    start_matching.delay(case_id)
    return case