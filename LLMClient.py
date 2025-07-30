import os
from dotenv import load_dotenv
import google.genai as genai
from openai import OpenAI
from time import sleep
import threading

class LLMClient:
    def __init__(self, provider, api_key=None):
        self.provider = provider
        self.client = None
        load_dotenv()

        if provider == "openai":
            openai_api_key = os.getenv("OPENAI_API_KEY_2")
            if not openai_api_key:
                raise ValueError("OpenAI API key not provided and OPENAI_API_KEY environment variable not set.")
            openai_client = OpenAI(api_key=openai_api_key)
            self.client = openai_client
            self.model = "gpt-4o-mini"
        elif provider == "gemini":
            gemini_api_key = os.getenv("GEMINI_API_KEY")
            if not gemini_api_key:
                raise ValueError("Gemini API key not provided and neither GOOGLE_API_KEY nor GEMINI_API_KEY environment variable set.")
            genai_client = genai.Client(api_key=gemini_api_key)
            self.client = genai_client
            self.model = "gemini-2.5-flash-lite"
        else:
            raise ValueError("Unsupported LLM provider. Choose 'openai' or 'gemini'.")

    def show_loading_bar(self, stop_event):
        print("Loading", end="", flush=True)
        while not stop_event.is_set():
            print(".", end="", flush=True)
            sleep(0.5)
        print(" done.")

    def chat(self, prompt, model=None, system_message=None):
        stop_event = threading.Event()
        loading_thread = threading.Thread(target=self.show_loading_bar, args=(stop_event,))
        loading_thread.start()

        try:
            if self.provider == "openai":
                messages = [{"role": "user", "content": prompt}]
                if system_message:
                    messages.insert(0, {"role": "system", "content": system_message})

                response = self.client.chat.completions.create(
                    model=model if model else self.model,
                    messages=messages
                )
                return response.choices[0].message.content

            elif self.provider == "gemini":
                full_prompt = f"{system_message}\n{prompt}" if system_message else prompt

                response = self.client.models.generate_content(
                    model=self.model,
                    contents=full_prompt,
                )

                if response.candidates:
                    first_candidate = response.candidates[0]
                    if first_candidate.content and first_candidate.content.parts:
                        for part in first_candidate.content.parts:
                            if hasattr(part, 'text'):
                                return part.text
                raise ValueError("No text is found.")
        finally:
            stop_event.set()
            loading_thread.join()