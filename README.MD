# Emotion-Aware Support Chatbot

A conversational AI that detects the emotional tone of what you say and adapts its response style accordingly — supportive when you're stressed, normal and friendly when you're not.

## Features
- Detects emotional state per message (stressed, sad, anxious, happy, neutral, etc.)
- Adapts tone: supportive + helpful during distress, casual otherwise
- Maintains conversation history for context
- Gently redirects to real support resources for crisis-level messages

## Tech Stack
- Python 3.14
- Google Gemini API (free tier)
- Gradio (chat UI)

## Setup

1. Clone this repo

git clone https://github.com/Arpita-e/emotion-aware-chatbot.git
cd emotion-aware-chatbot

2. Create a virtual environment

python -m venv venv
venv\Scripts\activate

3. Install dependencies

pip install -r requirements.txt

4. Get a free Gemini API key from https://aistudio.google.com/app/apikey

5. Create a `.env` file with:

GEMINI_API_KEY=your_key_here

6. Run the app

python main.py

## Disclaimer
This is a student project, not a substitute for real mental health support.

## Project Context
Built as a minor project for an AIML internship, exploring emotion detection and adaptive tone generation in conversational AI.