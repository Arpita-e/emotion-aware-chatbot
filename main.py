"""
Emotion-Aware Support Chatbot
AIML Internship - Minor Project
"""

import os
import json
import google.generativeai as genai
from dotenv import load_dotenv
import gradio as gr

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise ValueError(
        "GEMINI_API_KEY not found. Create a .env file and paste your free Gemini API key in it."
    )

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-3.1-flash-lite")

SYSTEM_PROMPT = """You are an emotionally-intelligent support companion.

For every message the user sends:
1. Silently detect their emotional state (e.g. stressed, sad, anxious, frustrated,
   happy, excited, neutral, overwhelmed).
2. Respond in a way that matches what they actually need:
   - If they show distress (sad/anxious/stressed/overwhelmed): respond warmly and
     supportively. Validate the feeling briefly, then be genuinely helpful -
     don't just repeat "I understand" with no substance. Keep it natural, not
     clinical or scripted.
   - If they're neutral or positive: respond like a normal, friendly conversational
     partner. Don't manufacture emotional intensity that isn't there.
3. Never diagnose, never claim to be a therapist, and if the user expresses serious
   crisis-level distress (self-harm, suicidal thoughts), gently encourage them to
   reach out to a real support line or trusted person - do not try to handle that
   yourself.
4. Keep responses conversational length (2-5 sentences), not essays.

After your reply, on a new line, output ONLY this JSON:
{"detected_emotion": "the emotion you detected"}
"""


def build_prompt(history, user_message):
    recent_history = history[-6:]  # only last 6 messages, not full history
    convo = ""
    for turn in recent_history:
        role = "User" if turn["role"] == "user" else "Assistant"
        convo += f"{role}: {turn['content']}\n"
    convo += f"User: {user_message}\nAssistant:"
    return f"{SYSTEM_PROMPT}\n\nConversation so far:\n{convo}"
   

def chat_fn(user_message, history):
    if not user_message.strip():
        return history, ""

    prompt = build_prompt(history, user_message)
    response = model.generate_content(
        prompt,
        generation_config={"max_output_tokens": 200}
    )
    raw = response.text.strip()

    reply_text = raw
    detected_emotion = None
    if "{" in raw and raw.rstrip().endswith("}"):
        json_start = raw.rfind("{")
        possible_json = raw[json_start:]
        try:
            parsed = json.loads(possible_json)
            detected_emotion = parsed.get("detected_emotion")
            reply_text = raw[:json_start].strip()
        except json.JSONDecodeError:
            pass

    if detected_emotion:
        reply_text += f"\n\n*(detected tone: {detected_emotion})*"

    history = history + [
        {"role": "user", "content": user_message},
        {"role": "assistant", "content": reply_text},
    ]
    return history, ""


with gr.Blocks(title="Emotion-Aware Support Chatbot") as demo:
    gr.Markdown(
        "# 💬 Emotion-Aware Support Chatbot\n"
        "Adapts its tone based on how you're feeling. Not a therapist - "
        "for real support, please reach out to a real person or helpline."
    )
    chatbot = gr.Chatbot(height=450)
    msg = gr.Textbox(label="Type a message", placeholder="How's your day going?")
    clear = gr.Button("Clear conversation")

    msg.submit(chat_fn, inputs=[msg, chatbot], outputs=[chatbot, msg])
    clear.click(lambda: ([], ""), outputs=[chatbot, msg])

    gr.Examples(
        examples=[
            "I bombed my interview today, I feel so stupid.",
            "Just got my internship results, I'm so excited!",
            "I've had a pretty normal day, nothing much happened.",
            "I'm really overwhelmed with deadlines this week and can't sleep properly.",
        ],
        inputs=msg,
    )


if __name__ == "__main__":
    demo.launch()