import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types
from config import *
from functions.get_files_info import schema_get_files_info
from functions.get_files_content import schema_get_files_content
from functions.run_python_file import schema_run_python_file
from functions.write_file import schema_write_file

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

def main():
    parser = argparse.ArgumentParser(description="Makes a call to Gemini API when a prompt is given")

    parser.add_argument("input", help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Adds additional information about the response")

    args = parser.parse_args()


    messages = [
        types.Content(role="user", parts=[types.Part(text=args.input)]),
    ]

    available_functions = types.Tool(
        function_declarations = [
            schema_get_files_info,
            schema_get_files_content,
            schema_run_python_file,
            schema_write_file,
        ]
    )


    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model="gemini-2.0-flash-001", 
        contents=messages,
        config=types.GenerateContentConfig(system_instruction=SYSTEM_PROMPT, tools=[available_functions])
    )

    if args.verbose:
        print(f"User prompt: {response.text}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    else:
        print(response.text)

        for fx in response.function_calls:
            print(f"Calling function: {fx.name}({fx.args})")


if __name__ == "__main__":
    main()
