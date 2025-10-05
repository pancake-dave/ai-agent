import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.run_python_file import schema_run_python_file
from functions.write_file import schema_write_file
from functions.call_function import call_function

def main():
    # Ensure a user prompt is provided as a command-line argument
    if len(sys.argv) < 2:
        sys.exit(1)

    # Load environment variables from .env file
    load_dotenv()
    # Retrieve Gemini API key for authentication
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    # First command-line argument is the user's request
    user_prompt = sys.argv[1]
    # System prompt defines agent behavior and available operations; can be adjusted for more specific agent use case
    system_prompt = """
                    You are a helpful AI coding agent.
                    
                    When a user asks a question or makes a request, make a function call plan. You can perform the following operations:
                    
                    - List files and directories
                    - Read file contents
                    - Execute Python files with optional arguments
                    - Write or overwrite files
                    
                    All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
                    """
    # Register available agent functions (tools) for the LLM (Gemini in this case) to call; to add functions create a module in /functions dir, import it and update the system prompt and available_functions object
    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_run_python_file,
            schema_write_file
        ]
    )
    # Initial message list containing the user's prompt
    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]
    # Enable verbose output if '--verbose' flag is present - this will tell you token usage and function calling feedback if any
    verbose = False
    if "--verbose" in sys.argv:
        verbose = True

    # Agent reasoning loop: iteratively interacts with Gemini and executes tool calls; restraining maximum number of iterations prevents LLM from endlessly looping
    max_iterations = 20
    for i in range(max_iterations):
        try:
            # Request Gemini to generate content based on current messages and available tools
            response = client.models.generate_content(
                model='gemini-2.0-flash-001',
                contents=messages,
                config=types.GenerateContentConfig(
                    tools=[available_functions],
                    system_instruction=system_prompt
                )
            )
            # Add each response candidate to messages for multi-turn reasoning
            for candidate in response.candidates:
                messages.append(candidate.content)

            if verbose:
                print(f"User prompt: {user_prompt}")
                print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
                print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
            # If Gemini returns a plain text response (no tool calls) that means it's done - print text response and exit
            if not response.function_calls and response.text:
                print(response.text)
                break

            # If Gemini returns function calls, execute each tool and feed the result back
            if response.function_calls:
                for function_call_part in response.function_calls:
                    function_call_result = call_function(function_call_part=function_call_part, verbose=verbose)
                    # Validate the tool response structure
                    if (
                        not function_call_result
                        or len(function_call_result.parts) < 1
                        or not hasattr(function_call_result.parts[0], "function_response")
                        or not hasattr(function_call_result.parts[0].function_response, "response")
                    ):
                        raise RuntimeError(f"Malformed tool response for {function_call_part.name}")
                    elif verbose:
                        print(f"-> {function_call_result.parts[0].function_response.response}")

                    # Send tool result back to Gemini for further reasoning - construct the types.Part for types.Content so it's understandable for the LLM and append to messages list
                    tool_resp = types.Part(
                        function_response=types.FunctionResponse(
                            name=function_call_part.name,
                            response=function_call_result.parts[0].function_response.response,
                        )
                    )

                    messages.append(types.Content(role="user", parts=[tool_resp]))
        except Exception as e:
            return f"Error: content generation failed due to: {e}"


if __name__ == "__main__":
    main()
