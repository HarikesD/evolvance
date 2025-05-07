import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def reflect_on_message(message: str) -> dict:
    """
    Returns either a reflective or not_reflective JSON.
    """
    prompt = f"""
You are a Reflection Agent.

Your role:
1. Assess if the message is reflective.
2. If reflective, output insight, reframe, agent_learning.
3. Otherwise prompt for deeper sharing.

User message:
\"\"\"{message}\"\"\"
"""
    try:
        resp = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are an emotionally intelligent counselor."},
                {"role": "user",   "content": prompt}
            ],
            temperature=0.6
        )
        return eval(resp.choices[0].message.content.strip())
    except Exception as e:
        print("🛠 Reflection Agent Error:", e)
        return {
            "status": "not_reflective",
            "agent_response": "I’m here if you’d like to explore something more personal or emotional."
        }
