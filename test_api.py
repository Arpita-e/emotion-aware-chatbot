import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
print("Key loaded:", bool(API_KEY))

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-3.8-flash")

print("Sending test request...")
response = model.generate_content("Say hello in one sentence.")
print("Response:", response.text)