import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_growth_challenge(mental_model: str, message: str) -> dict:
    prompt = f"""
You are a Growth Challenge Agent.

Decide if user is ready for a micro-challenge.

If yes, return JSON:
{{
  "status": "challenge",
  "micro_challenge": "...",
  "stretch_prompt": "...",
  "reminder": "in X days"
}}

If no, return JSON:
{{
  "status": "not_ready",
  "message": "..."
}}

Mental Model: {mental_model}
User Message:
\"\"\"{message}\"\"\"
"""
    try:
        resp = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a growth challenge engine."},
                {"role": "user",   "content": prompt}
            ],
            temperature=0.5
        )
        return eval(resp.choices[0].message.content.strip())
    except Exception as e:
        print("⚠️ Challenge generation failed:", e)
        return {"status": "not_ready", "message": "Something went wrong."}
