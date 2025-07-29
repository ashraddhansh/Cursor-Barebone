import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions import run_python
from functions.get_files_info import get_files_info, schema_get_files_info
from functions.write_file import schema_write_file, write_file
from functions.run_python import run_python_file, schema_run_python_file
from functions.get_file_content import get_file_content, schema_get_file_content


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

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file
    ]
)

function_map = {
        "write_file": write_file,
        "run_python_file": run_python_file,
        "get_files_info": get_files_info,
        "get_file_content": get_file_content
        }

def call_function(function_call_part, verbose = False):
    func_name = function_call_part.name
    func_args = function_call_part.args
    if verbose:
        print(f"Calling function: {function_call_part.name}({func_name})")
    else:
        print(f" - Calling function: {func_name}")

    if function_call_part.name not in function_map:
        return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name = func_name,
                response = {"error": f"Unknown function: {func_name}"},
            )
            ],
        )

    func_args["working_directory"] = "./calculator/"

    try:
        result = function_map[func_name](**func_args)
    except Exception as e:
        result = f"Function raised an exception: {e}"

    return types.Content(
    role="tool",
    parts=[
        types.Part.from_function_response(
            name=function_call_part.name,
            response={"result": result},
        )
    ],
)


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



if __name__ == "__main__":
    main()
