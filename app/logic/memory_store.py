store = {}

def get_user_session(user_id: str) -> dict:
    if user_id not in store:
        store[user_id] = {
            "step": 0,
            "answers": [],
            "questions": [
                "When you're stuck emotionally, what do you typically do?",
                "Have you recently had an insight about yourself?",
                "What kind of personal growth feels hardest for you right now?"
            ],
            "completed": False,
            "confidence": {
                "growth_challenge": 0.33,
                "reflection_agent": 0.33,
                "wisdom_capture": 0.33
            },
            "mental_model": None,
            "final_model": None,
            "final_agent": None,
            "valence_history": [],
            "emotion_stage": 2,
            "last_valence": 0.0
        }
    return store[user_id]

def set_mental_model(user_id: str, model: str):
    session = get_user_session(user_id)
    session["mental_model"] = model
