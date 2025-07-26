import os
from .constants import MAX_CHARS
from google.genai import types

def get_file_content(working_directory, file_path):
    try:
        joined_file_path = os.path.join(working_directory,file_path)
        abs_dir_path = os.path.abspath(working_directory)
        abs_file_path = os.path.abspath(joined_file_path)

        if not abs_file_path.startswith(abs_dir_path):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(abs_file_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        with open(abs_file_path, "r") as f:
            file_content = f.read(MAX_CHARS + 1)

            if len(file_content) > MAX_CHARS:
                file_content_string = file_content[:MAX_CHARS] + f'[...File "{file_path}" truncated at 10000 characters]'

            else:
                file_content_string = file_content
            return file_content_string

    except Exception as e:
        return f"Error: {e}"


schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Returns contents of the specified file, if file is larger then it is truncated at 10000 characters, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file to return content from, relative to the working directory.",
            ),
        },
        required=["file_path"]
    ),
)
