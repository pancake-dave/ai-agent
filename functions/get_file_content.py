import os
from functions.config import character_limit
from functions.normalize_paths import normalize_paths

def get_file_content(working_directory, file_path):
    try:
        working_path, full_path = normalize_paths(working_directory, file_path)
        if not os.path.commonpath([working_path, full_path]) == working_path:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        elif not os.path.isfile(full_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        with open(full_path, "r") as file:
            data = file.read()
            if len(data) > character_limit:
                return f'{data[:character_limit]} [...File "{file_path}" truncated at 10000 characters]'
            return data
    except Exception as e:
        return f"Error: {e}"