from google.genai import types
from functions.get_files_info import get_files_info, schema_get_files_info
from functions.write_file import schema_write_file, write_file
from functions.run_python import run_python_file, schema_run_python_file
from functions.get_file_content import get_file_content, schema_get_file_content
from config import WORKING_DIRECTORY

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
    func_args = dict(function_call_part.args)
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

    func_args["working_directory"] = WORKING_DIRECTORY

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
