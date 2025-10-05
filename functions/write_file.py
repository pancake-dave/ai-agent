import os
from functions.normalize_paths import normalize_paths
from google.genai import types

def write_file(working_directory, file_path, content):
    try:
        # Normalize and resolve absolute paths for safety
        working_path, full_path = normalize_paths(working_directory, file_path)
        # Prevent writing outside the permitted working directory
        if not os.path.commonpath([working_path, full_path]) == working_path:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        # Create parent directories if they do not exist
        if not os.path.exists(os.path.dirname(full_path)):
            os.makedirs(os.path.dirname(full_path))
        # Write content to the file (overwriting if it exists)
        with open(full_path, "w", encoding="utf-8") as file:
            file.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f"Error: {e}"

# Gemini tool schema describing the write_file function for the agent
schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Write data into a file of a specified path, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file to be written, relative to the working directory. This parameter has to be provided.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Data to be written into the file. This parameter has to be provided.",
            ),
        },
    ),
)