
import os
from dotenv import load_dotenv
from groq import Groq

# Force reload of .env
load_dotenv(override=True)

api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    print("❌ No API Key found.")
    exit(1)

client = Groq(api_key=api_key)

try:
    print("Fetching available models...")
    models = client.models.list()
    with open("models.txt", "w", encoding="utf-8") as f:
        f.write("Available Models:\n")
        for model in models.data:
            f.write(f"- {model.id}\n")
    print("✅ Models saved to models.txt")
except Exception as e:
    print(f"❌ Failed to list models: {e}")
