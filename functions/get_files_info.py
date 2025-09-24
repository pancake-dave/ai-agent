import os
from functions.normalize_paths import normalize_paths
from google.genai import types

def get_files_info(working_directory, directory="."):
    try:
        working_path, full_path = normalize_paths(working_directory, directory)
        if not os.path.commonpath([working_path, full_path]) == working_path:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        elif not os.path.isdir(full_path):
            return f'Error: "{directory}" is not a directory'

        result = []
        for item in os.listdir(full_path):
            current_path = os.path.join(full_path, item)
            result.append("- " + item + ": file_size=" + str(os.path.getsize(current_path)) + " bytes, is_dir=" + str(os.path.isdir(current_path)))
        return "\n".join(result)
    except Exception as e:
        return f"Error: {e}"

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