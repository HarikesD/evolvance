from fastapi import APIRouter
from app.models.reflection import ReflectionRequest, ReflectionResponse
from app.logic.reflection import reflect_on_message
import datetime

router = APIRouter(tags=["Reflection"])

@router.post("/process", response_model=ReflectionResponse)
def process_reflection(payload: ReflectionRequest):
    result = reflect_on_message(payload.message)
    return ReflectionResponse(
        user_id=payload.user_id,
        mental_model=payload.mental_model,
        insight=result.get("agent_response"),
        reframed_narrative=result.get("reframe", "Let’s keep unpacking that."),
        agent_learning=result.get("agent_learning", "Logged for future insight alignment."),
        timestamp=datetime.datetime.utcnow().isoformat()
    )
