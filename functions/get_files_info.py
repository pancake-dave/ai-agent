import os

def get_files_info(working_directory, directory="."):
    working_path = os.path.abspath(working_directory)
    full_path = os.path.abspath(os.path.join(working_directory, directory))
    if not full_path.startswith(working_path):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    elif not os.path.isdir(full_path):
        return f'Error: "{directory}" is not a directory'
    result = []
    for item in os.listdir(full_path):
        current_path = os.path.join(full_path, item)
        result.append("- " + item + ": file_size=" + str(os.path.getsize(current_path)) + " bytes, is_dir=" + str(os.path.isdir(current_path)))

    return "\n".join(result)


print(get_files_info("/home/dawid/bootdev", "ai-agent")) #debug