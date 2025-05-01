from fastapi import APIRouter
from app.models.growth_challenge import (
    GrowthChallengeRequest,
    GrowthChallengeChallengeResponse,
    GrowthChallengeNotReadyResponse,
)
from app.logic.generator import generate_growth_challenge
import datetime

router = APIRouter(tags=["Growth Challenge"])

@router.post("/process", response_model=dict)
def process_challenge(payload: GrowthChallengeRequest):
    result = generate_growth_challenge(payload.mental_model, payload.message)

    if result.get("status") == "challenge":
        return GrowthChallengeChallengeResponse(
            user_id=payload.user_id,
            mental_model=payload.mental_model,
            micro_challenge=result["micro_challenge"],
            stretch_prompt=result["stretch_prompt"],
            reminder=result["reminder"],
            agent="growth_challenge_agent",
            timestamp=datetime.datetime.utcnow().isoformat()
        ).dict()

    return GrowthChallengeNotReadyResponse(
        user_id=payload.user_id,
        message=result.get("message", "Not ready for a challenge yet."),
        agent="growth_challenge_agent",
        timestamp=datetime.datetime.utcnow().isoformat()
    ).dict()
