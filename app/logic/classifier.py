import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def evaluate_response(session: dict, user_answer: str) -> dict:
    """
    Routes and updates confidence based on user_answer.
    """
    question   = session["questions"][session["step"]]
    confidence = session["confidence"]
    prompt = f"""
You are a routing classifier.

User mental model: '{session['mental_model']}'.
Q: {question}
A: {user_answer}

Previous confidences: {confidence}

Return JSON confidences for growth_challenge, reflection_agent, wisdom_capture.
"""
    try:
        resp = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a routing classifier."},
                {"role": "user",   "content": prompt}
            ],
            temperature=0.4
        )
        return json.loads(resp.choices[0].message.content.strip())
    except Exception as e:
        print("⚠️ Routing classifier failed:", e)
        return confidence
