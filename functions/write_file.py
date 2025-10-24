import os
from google.genai import types

def write_file(working_directory, file_path, content):
    relative_path = os.path.join(working_directory, file_path)
    file_path = os.path.abspath(relative_path)
    file_dir_name = os.path.dirname(file_path)
    wd_abs_path = os.path.abspath(working_directory)

    if not os.path.exists(file_dir_name):
        os.mkdir(file_dir_name)

    if not file_path.startswith(wd_abs_path):
        error_msg = f"Error: cannot list '{file_path}' as it is outside the permitted working directory"
        return error_msg

    with open(file_path, "w") as f:
        f.write(content)
        return f"successfully wrote to '{file_path}' ({len(content)} characters written)"
    

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Write content into a file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path, relative to the working directory",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to be written in the file",
            ),
        },
    ),
)