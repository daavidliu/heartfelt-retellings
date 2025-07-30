from LLMClient import LLMClient

def run_gemini_example():
    try:
        # Create an instance for Gemini
        # It will automatically pick up the API key from the environment variable
        gemini_client = LLMClient(provider="gemini")

        # Example 1: Simple chat
        print("--- Gemini Simple Chat ---")
        prompt1 = "What is the capital of France?"
        response1 = gemini_client.chat(prompt1)
        print(f"Prompt: {prompt1}\nResponse: {response1}\n")

        # Example 2: Chat with a system message (will be prepended for Gemini)
        print("--- Gemini Chat with System Message ---")
        prompt2 = "Tell me about a famous Australian landmark."
        system_message2 = "You are a helpful assistant that provides concise answers."
        response2 = gemini_client.chat(prompt2, system_message=system_message2)
        print(f"System: {system_message2}\nPrompt: {prompt2}\nResponse: {response2}\n")

        # Example 3: Using a different model (if available and you configure it)
        # Note: 'gemini-1.5-pro' might have different access/pricing.
        # Make sure you have access to it for your API key.
        # print("--- Gemini Chat with Different Model ---")
        # prompt3 = "Explain quantum entanglement in simple terms."
        # response3 = gemini_client.chat(prompt3, model='gemini-1.5-pro')
        # print(f"Prompt: {prompt3}\nResponse (gemini-1.5-pro): {response3}\n")

    except ValueError as e:
        print(f"Configuration error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def run_chatgpt_example():
    try:
        openai_client = LLMClient(provider="openai")

        # Example 1: Simple chat
        print("--- ChatGPT Simple Chat ---")
        prompt1 = "What is the capital of France?"
        response1 = openai_client.chat(prompt1)
        print(f"Prompt: {prompt1}\nResponse: {response1}\n")

        # Example 2: Chat with a system message (will be prepended for Gemini)
        print("--- ChatGPT Chat with System Message ---")
        prompt2 = "Tell me about a famous Australian landmark."
        system_message2 = "You are a helpful assistant that provides concise answers."
        response2 = openai_client.chat(prompt2, system_message=system_message2)
        print(f"System: {system_message2}\nPrompt: {prompt2}\nResponse: {response2}\n")

        # Example 3: Using a different model (if available and you configure it)
        # Note: 'gemini-1.5-pro' might have different access/pricing.
        # Make sure you have access to it for your API key.
        # print("--- Gemini Chat with Different Model ---")
        # prompt3 = "Explain quantum entanglement in simple terms."
        # response3 = gemini_client.chat(prompt3, model='gemini-1.5-pro')
        # print(f"Prompt: {prompt3}\nResponse (gemini-1.5-pro): {response3}\n")

    except ValueError as e:
        print(f"Configuration error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    run_gemini_example()