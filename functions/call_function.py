from functions.get_files_content import get_file_content
from functions.get_files_info import get_files_info
from functions.run_python_file import run_python_file
from functions.write_file import write_file
from google.genai import types


def call_function(function_call, verbose=False):
    if verbose:
        print(f"Calling function: {function_call.name}({function_call.args})")
    else:
        print(f"Calling function: {function_call.name}")
    
    match function_call.name:
        case "get_file_content":
            fx_result = get_file_content(working_directory="./calculator", **function_call.args)
        case "get_files_info":
            fx_result = get_files_info(working_directory="./calculator", **function_call.args)
        case "run_python_file":
            fx_result = run_python_file(working_directory="./calculator", **function_call.args)
        case "write_file":
            fx_result = write_file(working_directory="./calculator", **function_call.args)
        case _:
            return types.Content(
                role="tool",
                parts=[
                    types.Part.from_function_response(
                        name=function_call.name,
                        response={"error": f"Unknown function: {function_call.name}"},
                    )
                ],
            )
    
    result = {"output": fx_result}
    
    return result