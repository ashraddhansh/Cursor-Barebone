import os
import sys
from dotenv import load_dotenv
from google import genai
load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

def main():
    if len(sys.argv) == 1:
        print("Usage: uv main.py \"Your prompt here\"")
        sys.exit(1)
    else:
        output = client.models.generate_content(model = "gemini-2.0-flash-001",contents=sys.argv[1])
        print(output.text)
        print(f"Prompt tokens: {output.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {output.usage_metadata.candidates_token_count}")


if __name__ == "__main__":
    main()
