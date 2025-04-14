
import requests
import json
import os
from dotenv import load_dotenv

# Loading the OpenRouter API key from .env file
load_dotenv()
API_KEY = os.getenv("API_KEY")

# Load memory from memory.json
def load_memory():
    if os.path.exists("memory.json"):
        try:
            with open("memory.json", "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {}
    return {}

# Save memory to memory.json, we will use json
def save_memory(memory):
    try:
        with open("memory.json", "w") as f:
            json.dump(memory, f, indent=4)
    except Exception as e:
        print(f"Error saving memory: {e}")

# Get response from Qwerky-72B (OpenRouter)   
def get_ai_response(user_prompt, memory=None):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    # Base messages to start the conversation
    messages = [
        {
            "role": "system",
            "content": "You are a helpful, intelligent, and friendly personal assistant. You remember important user information when shared and help with tasks like answering questions, setting reminders, and summarizing notes."
        }
    ]

    # Optional memory injection
    if memory and len(memory) > 0:
        memory_prompt = f"The user previously told you these things: {json.dumps(memory)}"
        messages.append({"role": "user", "content": memory_prompt})

    # Add the actual prompt from user
    messages.append({"role": "user", "content": user_prompt})

    # OpenRouter API request payload
    data = {
        "model": "qwen/qwen1.5-72b-chat",  # Qwerky-72B model name
        "messages": messages
    }

    # Send request to OpenRouter
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()  # Raise an error for bad status codes

        # Parse and return AI's response
        reply = response.json()
        return reply["choices"][0]["message"]["content"]

    except requests.exceptions.RequestException as e:
        print(" API Error:", e)
        return "Sorry, I couldn't connect to the AI service."

    except Exception as e:
        print(" Unexpected Error:", e)
        return "An error occurred while getting a response from the assistant."
