# ai-agent

### Hello there!

**ai-agent** is a guided project demonstrating the design and implementation of a modular AI coding agent. The agent interacts with code repositories, automates code-related operations, and leverages Google Gemini models for reasoning and tool use.

> **Security note:** this project includes basic guardrails, however since it's able to access and execute local files, user caution is recommended.

> **Explicit security note:** this agent can and will READ, OVERWRITE CONTENTS and RUN files from your computer.
## Overview

This project implements a command-line AI agent that can:
- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

The agent is designed to act as a coding assistant, making decisions and executing actions through a set of well-defined tools.

## Architecture

- **main.py**: Orchestrates agent reasoning, interaction with Gemini AI, and iterative tool use.
- **functions/**: Contains modular tools the agent can call:
  - `get_files_info.py`: Lists files/directories
  - `get_file_content.py`: Reads file content
  - `run_python_file.py`: Executes Python scripts
  - `write_file.py`: Writes to files
  - `call_function.py`: Handles tool invocation and responses
  - `normalize_paths.py`: Secures file path handling
  - `config.py`: Configuration helper

> **Note:** The `calculator/` directory is a dummy program for agent demonstration/testing and is not part of the agent’s core logic.

## Setup

1. Clone the repository.
2. Install [uv](https://github.com/astral-sh/uv) if you don’t have it:
   ```bash
   pip install uv
   ```
3. Install dependencies with uv:
   ```bash
   uv sync
   ```
4. Create a `.env` file in the root directory of the project with your Gemini API key (get one [here](https://aistudio.google.com/) if you don't have one already):
   ```
   GEMINI_API_KEY=your-key-here

## Usage

Run the agent with a user prompt:
```bash
python main.py "Show me the contents of main.py"
```
or if you want to use uv:
```bash
uv run main.py "Show me the contents of main.py"
```

Optional: add `--verbose` for debug information, like this:
```bash
uv run main.py "Show me the contents of main.py" --verbose
```

## Extending

To add new tools, create a new Python module in `functions/` and update the tool list in `main.py`.

## Testing

Manual tests can be run via `tests.py`:
```bash
python tests.py
```
or:
```bash
uv run tests.py
```
See inline comments for example function calls.

## License

This project is for educational purposes and provided as-is.
