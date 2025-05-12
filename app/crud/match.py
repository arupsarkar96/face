
from sqlalchemy.orm import Session, aliased
from app.models.case import Case
from app.models.match import Match


def crud_create_match(db: Session, source_case_id: str, matched_case_id: str, similarity: float):
    # Avoid self-match
    if source_case_id == matched_case_id:
        return None

    # Check for existing match
    existing = db.query(Match).filter_by(
        source_case_id=source_case_id,  # Convert UUID to string
        matched_case_id=matched_case_id  # Convert UUID to string
    ).first()

    if existing:
        return existing

    match = Match(
        source_case_id=source_case_id,  # Convert UUID to string
        matched_case_id=matched_case_id,  # Convert UUID to string
        similarity=similarity
    )
    db.add(match)
    db.commit()
    db.refresh(match)
    return match

async def crud_get_matches(db: Session, case_id: str):
    source_case = aliased(Case)
    matched_case = aliased(Case)

    matches = (
        db.query(
            Match.similarity,
            source_case.photo.label("source_photo"),
            matched_case.photo.label("matched_photo"),
            matched_case.name.label("matched_name"),
            matched_case.id.label("matched_id"),
            matched_case.phone.label("matched_phone"),
            matched_case.address.label("matched_address")
        )
        .join(source_case, source_case.id == Match.source_case_id)
        .join(matched_case, matched_case.id == Match.matched_case_id)
        .filter(Match.source_case_id == case_id)
        .order_by(Match.similarity.desc())
        .offset(0)
        .limit(1000)
        .all()
        )

    # matches = db.query(Match).filter(Match.source_case_id == case_id).all()
    return matches
