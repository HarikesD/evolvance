from pydantic import BaseModel

class ReflectionRequest(BaseModel):
    """
    Input for the Reflection agent.
    """
    user_id: str
    mental_model: str
    message: str

class ReflectionResponse(BaseModel):
    """
    Output of the Reflection agent.
    """
    user_id: str
    mental_model: str
    insight: str
    reframed_narrative: str
    agent_learning: str
    timestamp: str
