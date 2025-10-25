import os
from config import *
from google.genai import types


def get_file_content(working_directory, file_path):
    relative_path = os.path.join(working_directory, file_path)
    file_path = os.path.abspath(relative_path)
    wd_abs_path = os.path.abspath(working_directory)

    if not os.path.isfile(file_path):
        error_msg = f"Error: file not found or is not a regular file: '{file_path}'"
        return error_msg

    if not file_path.startswith(wd_abs_path):
        error_msg = f"Error: cannot list '{file_path}' as it is outside the permitted working directory"
        return error_msg
    
    with open(file_path, "r") as f:
        file_content = f.read(CHAR_LIMIT)

        if len(file_content) == CHAR_LIMIT:
            return file_content+f"[...File '{relative_path}' truncated at 10000 characters]"

        return file_content
    

schema_get_files_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Get a file content as a string, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path, relative to the working directory.",
            ),
        },
    ),
)