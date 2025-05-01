from pydantic import BaseModel

class WisdomCaptureRequest(BaseModel):
    """
    Input for the Wisdom Capture agent.
    """
    user_id: str
    mental_model: str
    message: str

class WisdomDetectedResponse(BaseModel):
    """
    Output when wisdom is detected.
    """
    user_id: str
    mental_model: str
    wisdom_entry: str
    trend_map: str
    growth_alert: str
    agent: str
    timestamp: str

class WisdomNotDetectedResponse(BaseModel):
    """
    Output when no wisdom is detected.
    """
    user_id: str
    message: str
    agent: str
    timestamp: str
