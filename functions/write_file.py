import os
from functions.normalize_paths import normalize_paths

def write_file(working_directory, file_path, content):
    try:
        working_path, full_path = normalize_paths(working_directory, file_path)
        if not os.path.commonpath([working_path, full_path]) == working_path:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        if not os.path.exists(os.path.dirname(full_path)):
            os.makedirs(os.path.dirname(full_path))
        with open(full_path, "w", encoding="utf-8") as file:
            file.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f"Error: {e}"