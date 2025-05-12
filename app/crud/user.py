from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import UserCreate


def crud_create_user(db: Session, user: UserCreate) -> User:
    existing_user = db.query(User).filter(User.email == user.email).first()

    if existing_user:
        # Update FCM if changed
        if user.fcm and existing_user.fcm != user.fcm:
            existing_user.fcm = user.fcm
            existing_user.photo = user.photo
            db.commit()
            db.refresh(existing_user)
        return existing_user

    # Create new user
    db_user = User(
        name=user.name,
        email=user.email,
        photo=user.photo,
        fcm=user.fcm
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_users(db: Session):
    return db.query(User).all()