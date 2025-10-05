import os
import subprocess
import sys
from functions.normalize_paths import normalize_paths
from google.genai import types

def run_python_file(working_directory, file_path, args=None):
    if args is None:
        args = []
    try:
        # Normalize and resolve absolute paths for safety
        working_path, full_path = normalize_paths(working_directory, file_path)
        # Prevent execution outside the permitted working directory
        if not os.path.commonpath([working_path, full_path]) == working_path:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        # Check if the script exists
        if not os.path.exists(full_path):
            return f'Error: File "{file_path}" not found.'
        # Ensure the file is a Python script
        if not full_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file.'

        # Run the Python script as a subprocess with optional arguments
        complete_process = subprocess.run(args=[sys.executable, full_path, *args],
                                          timeout=30, # Prevent long-running scripts
                                          capture_output=True, # Capture both stdout and stderr
                                          cwd=working_path,# Set working directory context
                                          text=True)
        # Collect output streams
        stdout = complete_process.stdout or ""
        stderr = complete_process.stderr or ""

        # Format the result output
        result = f"STDOUT: {stdout}\nSTDERR: {stderr}"
        # If error occurred (exit code is not 0), report exit code
        if complete_process.returncode != 0:
            result += f"\nProcess exited with code {complete_process.returncode}"
        # If no output at all, report this
        if not stdout and not stderr:
            return "No output produced."
        return result
    except Exception as e:
        return f"Error: executing Python file: {e}"

# Gemini tool schema describing the run_python_file function for the agent
schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Run python script of a specified path, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the script that is to be run, relative to the working directory. This parameter has to be provided.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="List of arguments for the script to run with. This parameter is optional.",
                items=types.Schema(type=types.Type.STRING)
            ),
        },
    ),
)