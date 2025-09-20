import os
from functions.config import character_limit

def get_file_content(working_directory, file_path):
    try:
        working_path = os.path.abspath(working_directory)
        full_path = os.path.abspath(os.path.join(working_directory, file_path))
        if not full_path.startswith(working_path):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        elif not os.path.isfile(full_path):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        with open(full_path, "r") as file:
            data = file.read()
            if len(data) > character_limit:
                return f'{data[:character_limit]} [...File "{file_path}" truncated at 10000 characters]'
            return data
    except Exception as e:
        return f"Error: {e}"