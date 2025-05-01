import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def capture_wisdom(mental_model: str, message: str) -> dict:
    """
    Returns wisdom_detected or no_wisdom JSON.
    """
    prompt = f"""
You are a Wisdom Capture Agent.

If message contains insight, return:
{{
  "status": "wisdom_detected",
  "wisdom_summary": "...",
  "trend_map": "...",
  "breakthrough_alert": "..."
}}

Else return:
{{ "status": "no_wisdom", "message": "…" }}

Mental Model: {mental_model}
User Message:
\"\"\"{message}\"\"\"
"""
    try:
        resp = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a wise insight synthesizer."},
                {"role": "user",   "content": prompt}
            ],
            temperature=0.5
        )
        return eval(resp.choices[0].message.content.strip())
    except Exception as e:
        print("Wisdom Capture Agent Error:", e)
        return {"status": "no_wisdom", "message": "Unable to process message at this time."}
