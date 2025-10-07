import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types

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

    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(model="gemini-2.0-flash-001", contents=messages)

    if args.verbose:
        print(f"User prompt: {response.text}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    else:
        print(response.text)


if __name__ == "__main__":
    main()
