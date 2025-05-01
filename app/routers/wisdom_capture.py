from fastapi import APIRouter
from app.models.wisdom_capture import (
    WisdomCaptureRequest,
    WisdomDetectedResponse,
    WisdomNotDetectedResponse
)
from app.logic.wisdom_capture import capture_wisdom
import datetime

router = APIRouter(tags=["Wisdom Capture"])

@router.post("/process", response_model=dict)
def process_wisdom(payload: WisdomCaptureRequest):
    result    = capture_wisdom(payload.mental_model, payload.message)
    timestamp = datetime.datetime.utcnow().isoformat()

    if result.get("status") == "wisdom_detected":
        return WisdomDetectedResponse(
            user_id=payload.user_id,
            mental_model=payload.mental_model,
            wisdom_entry=result["wisdom_summary"],
            trend_map=result["trend_map"],
            growth_alert=result["breakthrough_alert"],
            agent="wisdom_capture_agent",
            timestamp=timestamp
        ).dict()

    return WisdomNotDetectedResponse(
        user_id=payload.user_id,
        message=result.get("message", "Unable to capture wisdom."),
        agent="wisdom_capture_agent",
        timestamp=timestamp
    ).dict()
