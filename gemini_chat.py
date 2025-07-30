from google import genai
import os
from dotenv import load_dotenv

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=GEMINI_API_KEY)

def chat():
    print("Gemini Chatbot (type 'exit' to quit)")
    history = []
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break
        history.append(user_input)
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=history,
        )
        print("Gemini:", response.candidates[0].content.parts[0].text)
        history.append(response.candidates[0].content.parts[0].text)

if __name__ == "__main__":
    chat()