import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from call_function import call_function, available_functions


load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""



def main():
    if len(sys.argv) == 1:
        print("Usage: uv main.py \"Your prompt here\"")
        sys.exit(1)
    else:
        user_prompt = sys.argv[1]
        messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
        ]
        output = client.models.generate_content(
                model = "gemini-2.0-flash-001",
                contents=messages,
                config=types.GenerateContentConfig(
                    tools=[available_functions],
                    system_instruction=system_prompt)
                )

        if output.function_calls:
            for function_call_part in output.function_calls:
                function_call_result = call_function(function_call_part,verbose="--verbose" in sys.argv)

                try:
                    response = function_call_result.parts[0].function_response.response
                except (AttributeError, IndentationError):
                    raise RuntimeError("Fatal: No function response found in tool output")

                if "--verbose" in sys.argv:
                    print(f"-> {response}")
        if output.text:
            print(output.text)



if __name__ == "__main__":
    main()
