import os.path
from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file
from functions.run_python_file import run_python_file

# Manual test script for agent tool functions.
# Uncomment print statements to run individual tests and observe their output.

##Test listing files/directories in various locations
# print(get_files_info("calculator", "."))
# print(get_files_info("calculator", "pkg"))
# print(get_files_info("calculator", "/bin"))
# print(get_files_info("calculator", "../"))

## Test reading file content from different paths
# print(get_file_content("calculator", "lorem.txt"))
# print(get_file_content("calculator", "main.py"))
# print(get_file_content("calculator", "pkg/calculator.py"))
# print(get_file_content("calculator", "/bin/cat"))
# print(get_file_content("calculator", "pkg/does_not_exist.py"))

## Test writing to files, including valid and invalid locations
# print(write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum"))
# print(write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet"))
# print(write_file("calculator", "/tmp/temp.txt", "this should not be allowed"))

## Test running Python scripts with and without arguments, and error cases
# print(run_python_file("calculator", "main.py"))
# print(run_python_file("calculator", "main.py", ["3 + 5"]))
# print(run_python_file("calculator", "tests.py"))
# print(run_python_file("calculator", "../main.py"))
# print(run_python_file("calculator", "nonexistent.py"))