import os
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path, args=[]):
    filename = file_path
    relative_path = os.path.join(working_directory, file_path)
    file_path = os.path.abspath(relative_path)
    wd_abs_path = os.path.abspath(working_directory)

    if not file_path.startswith(wd_abs_path):
        error_msg = f'Error: Cannot execute "{filename}" as it is outside the permitted working directory'
        return error_msg
    
    if not os.path.isfile(file_path):
        error_msg = f'Error: File "{filename}" not found'
        return error_msg
    
    file_extension = relative_path.split(".")[-1]

    if file_extension != "py":
        return f"Error: '{file_path}' is not a python file"
    
    
    try:
        cmd = ["python", file_path, *args]

        result = subprocess.run(
            cmd,
            timeout=30, 
            capture_output=True,
            text = True
        )

        if result.returncode != 0:
            return (
                f"STDOUT:\n{result.stdout}\n"
                f"STDERR:\n{result.stderr}"
                f"Process exited with code{result.returncode}"
            )
        
        if not result.stdout.strip() and not result.stderr.strip():
            return "No output produced"

        return (
            f"STDOUT:\n{result.stdout}\n"
            f"STDERR:\n{result.stderr}"
        )
    
    except Exception as e:
        return f"Error: executing Python file: {e}"


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Execute a python file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path of the python file, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.STRING,
                description="Arguments used to run the python file. This parameter is optional, so if any argument is provided, just run the file without args.",
            ),
        },
    ),
)