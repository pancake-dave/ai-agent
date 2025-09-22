import os
import subprocess
import sys
from functions.normalize_paths import normalize_paths

def run_python_file(working_directory, file_path, args=None):
    if args is None:
        args = []
    try:
        working_path, full_path = normalize_paths(working_directory, file_path)
        if not os.path.commonpath([working_path, full_path]) == working_path:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.exists(full_path):
            return f'Error: File "{file_path}" not found.'
        if not full_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file.'

        complete_process = subprocess.run(args=[sys.executable, full_path, *args],
                                          timeout=30,
                                          capture_output=True,
                                          cwd=working_path,
                                          text=True)
        stdout = complete_process.stdout or ""
        stderr = complete_process.stderr or ""

        result = f"STDOUT: {stdout}\nSTDERR: {stderr}"
        if complete_process.returncode != 0:
            result += f"\nProcess exited with code {complete_process.returncode}"
        if not stdout and not stderr:
            return "No output produced."
        return result
    except Exception as e:
        return f"Error: executing Python file: {e}"