from pydantic import BaseModel

class UserMessage(BaseModel):
    """
    Payload for the Form-Of-Mind agent.
    """
    user_id: str
    message: str
