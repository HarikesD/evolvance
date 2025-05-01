import os
import openai
import json
from typing import Dict, Optional
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def get_valence_score(message: str) -> float:
    """
    Uses GPT to analyze emotional valence. Returns −1.0..1.0.
    """
    prompt = f"""
Rate the emotional valence of the following message on a scale from -1.0 (very negative)
to 1.0 (very positive). Return ONLY the number.

Message: "{message}"
"""
    try:
        resp = openai.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a valence scoring assistant."},
                {"role": "user",   "content": prompt}
            ],
            temperature=0.2
        )
        return float(resp.choices[0].message.content.strip())
    except Exception as e:
        print("⚠️ Valence scoring failed:", e)
        return 0.0

def update_emotion_stage(session: dict):
    """
    Updates emotion_stage (2–5) based on last 5 valence scores.
    """
    history = session.get("valence_history", [])
    if not history:
        return
    recent = history[-5:]
    avg = sum(recent) / len(recent)
    if avg <= -0.4:
        session["emotion_stage"] = 2
    elif avg < 0.2:
        session["emotion_stage"] = 3
    elif avg < 0.6:
        session["emotion_stage"] = 4
    else:
        session["emotion_stage"] = 5

def evaluate_confidence(question: str, answer: str, current: Dict[str, float]) -> Dict[str, float]:
    """
    Uses GPT to adjust confidences for each agent.
    """
    prompt = f"""
You are a confidence engine.

Q: {question}
A: {answer}

Previous confidences: {current}

Return JSON with updated confidences for growth_challenge, reflection_agent, wisdom_capture.
"""
    try:
        resp = openai.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a confidence assistant."},
                {"role": "user",   "content": prompt}
            ],
            temperature=0.4
        )
        return json.loads(resp.choices[0].message.content.strip())
    except Exception as e:
        print("⚠️ GPT Evaluation Failed:", e)
        return current

def smooth_confidence(old: Dict[str, float], new: Dict[str, float]) -> Dict[str, float]:
    """
    Averages old & new confidences.
    """
    return {k: round((old[k] + new.get(k,0)) / 2, 3) for k in old}

def get_top_model(confidence: Dict[str, float], threshold: float = 0.85) -> Optional[str]:
    """
    Returns the model name if any confidence ≥ threshold.
    """
    for model, score in confidence.items():
        if score >= threshold:
            return model
    return None

def generate_next_question(session: dict) -> str:
    """
    Uses GPT to generate the next question.
    """
    prev_qas = "\n".join(f"Q: {q}\nA: {a}" for q,a in zip(session["questions"], session["answers"]))
    prompt = f"""
Your mental model: '{session['mental_model']}'.

Previous Q&A:
{prev_qas}

Confidence: {session['confidence']}

Generate the next open-ended question. Return ONLY the question text.
"""
    try:
        resp = openai.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a growth conversation engine."},
                {"role": "user",   "content": prompt}
            ],
            temperature=0.7
        )
        return resp.choices[0].message.content.strip()
    except Exception as e:
        print("⚠️ GPT Question Generation Failed:", e)
        return "What has been emotionally significant to you recently?"
