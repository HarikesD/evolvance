from pydantic import BaseModel

class GrowthChallengeRequest(BaseModel):
    """
    Input for the Growth Challenge agent.
    """
    user_id: str
    mental_model: str
    message: str

class GrowthChallengeChallengeResponse(BaseModel):
    """
    Output when a micro-challenge is generated.
    """
    user_id: str
    mental_model: str
    micro_challenge: str
    stretch_prompt: str
    reminder: str
    agent: str
    timestamp: str

class GrowthChallengeNotReadyResponse(BaseModel):
    """
    Output when the user isn’t ready for a challenge.
    """
    user_id: str
    message: str
    agent: str
    timestamp: str
