import os
from google.genai import types

def get_files_info(working_directory, directory="."):
    relative_path = os.path.join(working_directory, directory)
    d_abs_path = os.path.abspath(relative_path)
    wd_abs_path = os.path.abspath(working_directory)

    if not os.path.isdir(d_abs_path):
        error_msg = f"Error: '{directory}' is not a directory"
        return error_msg

    if not d_abs_path.startswith(wd_abs_path):
        error_msg = f"Error: cannot list '{directory}' as it is outside the permitted working directory"
        return error_msg
    
    item_list = os.listdir(d_abs_path)

    if directory == ".":
        dir_name = "current"
    else:
        dir_name = f"'{directory}'"

    print(f"Result for {dir_name} directory:")
    for item in item_list:
        item_path = os.path.join(d_abs_path, item)
        item_size = os.path.getsize(item_path)
        is_dir = os.path.isdir(item_path)
        print(f"- {item}: file_size={item_size}, is_dir={is_dir}")


schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)
