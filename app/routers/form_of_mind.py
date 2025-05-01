from fastapi import APIRouter, HTTPException
from app.models.form_of_mind import UserMessage
from app.logic.memory_store import get_user_session, set_mental_model
from app.logic.conversation_flow import (
    evaluate_confidence,
    smooth_confidence,
    get_top_model,
    generate_next_question,
    get_valence_score,
    update_emotion_stage
)
import datetime

router = APIRouter(tags=["Form of Mind"])
MAX_STEPS, MIN_STEPS = 5, 2

@router.post("/process")
def process_message(payload: UserMessage):
    user_id, message = payload.user_id, payload.message
    session = get_user_session(user_id)

    if session["completed"]:
        return {
            "user_id": user_id,
            "status": "completed",
            "form_of_mind": session["final_model"],
            "route_to": session["final_agent"],
            "confidence": session["confidence"],
            "emotion_stage": session["emotion_stage"],
            "timestamp": datetime.datetime.utcnow().isoformat()
        }

    current_q = session["questions"][-1] if session["questions"] else None
    if not current_q:
        raise HTTPException(status_code=400, detail="No active question in session.")

    conf_update = evaluate_confidence(current_q, message, session["confidence"])
    session["confidence"] = smooth_confidence(session["confidence"], conf_update)
    session["answers"].append(message)
    session["step"] += 1

    valence = get_valence_score(message)
    session["valence_history"].append(valence)
    session["last_valence"] = valence
    update_emotion_stage(session)

    final_model = get_top_model(session["confidence"], threshold=0.85)
    if final_model or session["step"] >= MAX_STEPS:
        session["completed"]   = True
        session["final_model"] = final_model or max(session["confidence"], key=session["confidence"].get)
        session["final_agent"] = (
            "reflection" if session["final_model"] == "Pattern Seeker"
            else "growth_challenge" if session["final_model"] == "Curious Observer"
            else "wisdom_capture"
        )
        set_mental_model(user_id, session["final_model"])
        return {
            "user_id": user_id,
            "status": "completed",
            "form_of_mind": session["final_model"],
            "route_to": session["final_agent"],
            "confidence": session["confidence"],
            "emotion_stage": session["emotion_stage"],
            "timestamp": datetime.datetime.utcnow().isoformat()
        }

    next_q = generate_next_question(session)
    session["questions"].append(next_q)
    return {
        "user_id": user_id,
        "status": "in_progress",
        "question": next_q,
        "step": session["step"],
        "confidence": session["confidence"],
        "emotion_stage": session["emotion_stage"],
        "timestamp": datetime.datetime.utcnow().isoformat()
    }
