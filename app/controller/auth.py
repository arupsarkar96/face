
from sqlalchemy.orm import Session
from google.oauth2 import id_token
from google.auth.transport import requests as grequests
from starlette.responses import JSONResponse
from app.schemas.auth import AuthResponse
from app.core.config import settings
from app.core.security import create_jwt_token
from app.schemas.user import UserCreate
from app.crud.user import crud_create_user


def authenticate_user(token: str, fcm: str, db: Session):
    try:
        info = id_token.verify_oauth2_token(token, grequests.Request(), settings.GOOGLE_CLIENT_ID)
        email = info["email"]
        name = info["name"]
        photo = info["picture"]

        create = UserCreate(name=name, email=email, photo=photo, fcm=fcm)
        user = crud_create_user(db, create)

        jwt_token = create_jwt_token(sub=user.email)
        return AuthResponse(id=user.id, email=user.email, name = user.name, photo=user.photo, token=jwt_token)
    except ValueError as e:
        return JSONResponse(status_code=401, content={"error": "Invalid Google token", "detail": str(e)})
