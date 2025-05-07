import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_growth_challenge(mental_model: str, message: str) -> dict:
    prompt = """You are a Growth Challenge Agent — a wise and emotionally intelligent guide who supports users on their personal growth journey.

Your job:
1. Read the user's current message in the context of their mental model.
2. Evaluate if they are ready for a new **growth micro-challenge** based on emotional tone, language, and mindset.
3. If they are ready, return a JSON object with:
{{
  "status": "challenge",
  "micro_challenge": "A realistic, emotionally aligned action to take within 1–3 days",
  "stretch_prompt": "A deep question to reflect on while engaging in the challenge",
  "reminder": "in X days"  // Suggest when to check back
}}

4. If they are **not ready**, return:
{{
  "status": "not_ready",
  "message": "An empathetic explanation or encouragement to first gain clarity or stability"
}}

Important:
- Make every challenge and prompt feel **custom, human, and caring**
- Do not sound robotic or overly generic
- Help the user feel **seen, supported, and slightly stretched**
- Reflect their mental model and emotional readiness

Mental Model: {mental_model}

User Message:
\"\"\"{message}\"\"\"

ONLY return valid JSON. No explanation or commentary.
""" 

    try:
        resp = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": "You are a compassionate coach that guides personal growth with micro-challenges and reflective prompts."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            
        )
        return json.loads(resp.choices[0].message.content.strip())
    except Exception as e:
        print("⚠️ Challenge generation failed:", e)
        return {
            "status": "not_ready",
            "message": "I'm here when you're ready for the next small step forward."
        }
