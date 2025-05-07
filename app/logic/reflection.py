import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def reflect_on_message(message: str) -> dict:
    """
    Generates a humility-centered reflection prompt with empathy + a deep question.
    Returns a JSON object guiding the user toward deeper understanding.
    """
    prompt = f"""
You are a Reflection Agent.

Your role is not to solve the user's problem, but to inspire reflective thinking through gentle, humility-centered questioning. Your presence should feel safe, wise, and emotionally aware.

Instructions:
1. Read the user's message and understand its emotional tone (e.g., frustration, sadness, regret, confusion, hope).
2. Respond with a short, emotionally attuned message that:
   - Validates what they’re going through without judgment
   - Shows understanding of their emotional state
3. Follow this with a humility-centered open-ended question that encourages self-exploration or rethinking. The goal is to help the user understand themselves, not to provide solutions.

Return a JSON object with:
{{
  "status": "reflective_prompt",
  "agent_response": "Empathic reflection + a meaningful question"
}}

Do not return anything else. No commentary. Only valid JSON.

User message:
\"\"\"{message}\"\"\"
"""

    try:
        resp = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": "You are an emotionally intelligent counselor who helps users reflect on their emotional experiences."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.6
        )
        content = resp.choices[0].message.content.strip()
        return json.loads(content)
    except Exception as e:
        print("🛠 Reflection Agent Error:", e)
        return {
            "status": "not_reflective",
            "agent_response": "I’m here if you’d like to explore what’s really on your mind. There’s no rush."
        }
