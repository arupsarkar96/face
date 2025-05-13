
import faiss
import numpy as np
import logging

from sqlalchemy.orm import Session
from app.core.celery import app
from app.db.session import SessionLocal
from app.models.case import Case
from app.crud.match import crud_create_match  # Assuming you have this



from app.models.user import User
from app.services.firebase import firebase_send_to_token

# Constants
EMBEDDING_DIM = 128
BATCH_SIZE = 250
MATCH_THRESHOLD = 0.5  # Cosine similarity threshold (0.5 = 50%)

# Setup FAISS
index = faiss.IndexFlatL2(EMBEDDING_DIM)

@app.task
def start_matching(case_id: str):
    logging.info(f"[Worker] 🔍 START MATCHING for Case ID: {case_id}")

    db: Session = SessionLocal()

    try:
        # Get the reference case
        reference_case = db.query(Case).filter(Case.id == str(case_id)).first()
        if not reference_case or not reference_case.data:
            logging.warning(f"❌ Case {case_id} not found or missing embedding.")
            return

        query_emb = np.array(reference_case.data, dtype=np.float32)
        query_emb = np.expand_dims(query_emb, axis=0)

        # Initialize matching
        offset = 0
        total_matches = 0
        batch_num = 1

        while True:
            batch = (
                db.query(Case)
                .filter(
                    Case.id != case_id,
                    Case.data.isnot(None),
                    Case.type != reference_case.type,
                )
                .offset(offset)
                .limit(BATCH_SIZE)
                .all()
            )

            if not batch:
                break

            logging.info(f"📦 Batch #{batch_num} | Records: {len(batch)}")

            index.reset()
            id_map = []
            emb_list = []

            for case in batch:
                emb = np.array(case.data, dtype=np.float32)
                if emb.shape[0] != EMBEDDING_DIM:
                    continue
                emb_list.append(emb)
                id_map.append((case.id, case.name, emb))

            if not emb_list:
                offset += BATCH_SIZE
                batch_num += 1
                continue

            index.add(np.stack(emb_list))
            D, I = index.search(query_emb, k=len(id_map))

            for i, dist in zip(I[0], D[0]):
                if i == -1 or i >= len(id_map):
                    continue

                matched_id, matched_name, matched_emb = id_map[i]

                # Compute cosine similarity
                cosine_sim = np.dot(query_emb[0], matched_emb) / (
                    np.linalg.norm(query_emb[0]) * np.linalg.norm(matched_emb)
                )

                if cosine_sim >= MATCH_THRESHOLD:
                    match_percent = round(cosine_sim * 100, 2)
                    logging.info(f"✅ Match: {matched_id} ({matched_name}) → {match_percent}%")
                    crud_create_match(db, case_id, matched_id, match_percent)
                    # Add for opposite too
                    crud_create_match(db, matched_id, case_id, match_percent)
                    formatted_percent = f"{match_percent:.2f}"
                    send_push_notification.delay(
                        case_id=matched_id,
                        title="💡 You've Got a New Match!",
                        body=f"🔗 A case has matched with {formatted_percent}% similarity. Check it out now!"
                    )
                    total_matches += 1

            offset += BATCH_SIZE
            batch_num += 1

        logging.info(f"🎯 Finished matching. Total matches: {total_matches}")
        if total_matches > 0:
            send_push_notification.delay(
                case_id=case_id,
                title="🎯 Matching Complete!",
                body=f"✅ We found {total_matches} potential match{'es' if total_matches > 1 else ''}!"
            )
        else:
            send_push_notification.delay(
                case_id=case_id,
                title="⏳ Still Searching...",
                body="We couldn't find a match right now. We're keeping an eye out and will notify you soon!"
            )


    except Exception as e:
        db.rollback()
        logging.error(f"💥 Matching failed: {str(e)}", exc_info=True)
    finally:
        db.close()

@app.task
def send_push_notification(case_id: str, title: str, body: str):
    logging.info(f"[Worker] 🔍 PUSH for Case ID: {case_id}")
    db: Session = SessionLocal()

    try:
        reference_case = db.query(Case).filter(Case.id == str(case_id)).first()
        if not reference_case:
            logging.warning(f"❌ Case {case_id} not found")
            return
        reference_user = db.query(User).filter(User.email == reference_case.user_id).first()
        if not reference_user or not reference_user.fcm:
            logging.warning(f"❌ User {reference_case.user_id} not found")
            return
        firebase_send_to_token(registration_token=reference_user.fcm, title=title, body=body)
    except Exception as e:
        db.rollback()
        logging.error(f"💥 Notify failed: {str(e)}", exc_info=True)
    finally:
        db.close()
