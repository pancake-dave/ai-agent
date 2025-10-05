import os
from functions.config import character_limit
from functions.normalize_paths import normalize_paths
from google.genai import types

def get_file_content(working_directory, file_path):
    try:
        # Normalize and resolve absolute paths for safety
        working_path, full_path = normalize_paths(working_directory, file_path)
        # Prevent reading files outside the permitted working directory
        if not os.path.commonpath([working_path, full_path]) == working_path:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        # Check if the file exists and is a regular file
        elif not os.path.isfile(full_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        # Read the file contents
        with open(full_path, "r") as file:
            data = file.read()
            # Truncate output if file is too large - see config.py for character limit
            if len(data) > character_limit:
                return f'{data[:character_limit]} [...File "{file_path}" truncated at {character_limit} characters]'
            return data
    except Exception as e:
        return f"Error: {e}"

# Gemini tool schema describing the get_file_content function for the agent
schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Read file contents of a specified path, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path leading to the file that is to be read, relative to the working directory. This parameter has to be provided.",
            ),
        },
    ),
)