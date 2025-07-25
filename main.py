import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

def main():
    if len(sys.argv) == 1:
        print("Usage: uv main.py \"Your prompt here\"")
        sys.exit(1)
    else:
        user_prompt = sys.argv[1]
        messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
        ]
        output = client.models.generate_content(model = "gemini-2.0-flash-001",contents=messages)
        print(output.text)

    if "--verbose" in sys.argv:
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {output.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {output.usage_metadata.candidates_token_count}")


if __name__ == "__main__":
    main()
