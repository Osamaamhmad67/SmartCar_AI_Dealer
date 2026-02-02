
import os
from dotenv import load_dotenv
from groq import Groq

# Force reload of .env
load_dotenv(override=True)

api_key = os.getenv("GROQ_API_KEY")
print(f"Testing Key: {api_key[:10]}...{api_key[-5:] if api_key else ''} (Length: {len(api_key) if api_key else 0})")

if not api_key:
    print("❌ No API Key found.")
    exit(1)

client = Groq(api_key=api_key)

try:
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": "Hello",
            }
        ],
        model="meta-llama/llama-4-scout-17b-16e-instruct",
    )
    print("✅ Connection Successful!")
    print(f"Response: {chat_completion.choices[0].message.content}")
except Exception as e:
    print(f"❌ Connection Failed: {e}")
