from google.genai import types
from functions.config import working_directory
from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.run_python_file import run_python_file
from functions.write_file import write_file

def call_function(function_call_part, verbose=False):
    # Extract function name from Gemini's function call part
    function_name = function_call_part.name
    # Prepare arguments for the function (empty dict if none provided)
    if not function_call_part.args:
        function_args = {}
    else:
        function_args = function_call_part.args
    # Always provide working directory as argument (for convenience stored in config file) - this is done for safety reasons
    function_args["working_directory"] = working_directory
    # Verbose/debug output for function calls
    if verbose:
        print(f"Calling function: {function_name}({function_args})")
    else:
        print(f" - Calling function: {function_name}")

    # Map function names to actual Python implementations
    function_call = {
        "get_files_info" : get_files_info,
        "get_file_content" : get_file_content,
        "run_python_file" : run_python_file,
        "write_file" : write_file
    }
    try:
        # Dynamically execute the selected function with provided arguments
        function_result = function_call[function_name](**function_args)
        # Return Gemini-compatible tool response content object
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"result": function_result},
                )
            ],
        )
    except KeyError:
        # Handle case where function name is unknown
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )
