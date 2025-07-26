import os
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path, args=[]):
    full_file_path = os.path.join(working_directory,file_path)
    abs_file_path = os.path.abspath(full_file_path)
    abs_dir_path = os.path.abspath(working_directory)

    if not abs_file_path.startswith(abs_dir_path):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.exists(abs_file_path):
        return f'Error: File "{file_path}" not found.'
    if not abs_file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'
    try:
        completed_process = subprocess.run(["python3",file_path, *args],capture_output= True, timeout= 30, cwd=abs_dir_path, text=True)

        output = []
        if completed_process.stdout:
            output.append(f"STDOUT:\n{completed_process.stdout}")

        if completed_process.stderr:
            output.append(f"STDERR:\n{completed_process.stderr}")

        if completed_process.returncode != 0:
            output.append(f"Process exited with code {completed_process.returncode}")

        return "\n".join(output) if output else "No output produced."


    except Exception as e:
        return f"Error: executing python file: {e}"


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python file located inside the working directory with optional command-line arguments, and returns its stdout and stderr output.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Relative path to the Python file inside the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="Optional list of arguments to pass to the Python script.",
                items=types.Schema(type=types.Type.STRING)
            )
        },
        required=["file_path"]
    ),
)
