from sqlalchemy.orm import Session

from app.models.case import Case


def crud_create_case(db: Session, case: Case):
    db.add(case)
    db.commit()
    db.refresh(case)
    return case

def crud_get_cases(db: Session, user: str):
    return (db.query(Case)
            .filter(Case.user_id == user)
            .order_by(Case.created_at.desc())
            .all())
