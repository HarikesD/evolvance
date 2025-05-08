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
    prompt = prompt = f"""
You are a highly skilled Reflection Agent, expert in active listening, emotional intelligence, and cognitive reframing.

Your objectives:
1. Identify whether the user’s message shows genuine self-reflection.
2. If it is reflective:
   a. Summarize the core insight in 1–2 sentences.
   b. Detect the primary emotion(s) expressed.
   c. Offer a supportive reframing suggestion to open new perspectives.
   d. Pose a thoughtful follow-up question to deepen their reflection.
   e. Respond with a JSON object:
      {{
        "status": "reflective",
        "insight_summary": "...",
        "emotional_tone": "...",
        "reframe_suggestion": "...",
        "next_question": "..."
      }}
3. If it is not reflective:
   a. Reply with an empathetic invitation for deeper sharing.
   b. Respond with a JSON object:
      {{
        "status": "not_reflective",
        "agent_response": "I’m here to listen—would you like to share more about what’s on your mind or how you’re feeling?"
      }}
4. Do not include any extra text—return only the JSON.

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
