import os

class PathCheckError(Exception):
    pass

def normalize_paths(working_directory, target_path):
    try:
        working_path = os.path.realpath(os.path.abspath(working_directory))
        full_path = os.path.realpath(os.path.abspath(os.path.join(working_directory, target_path)))
        return working_path, full_path
    except ValueError as e:  # e.g., different drives on Windows
        raise PathCheckError(f"base and target are on different roots: base={working_directory!r}, target={target_path!r}") from e
    except Exception as e:
        raise RuntimeError(f"path check failed for base={working_directory!r}, target={target_path!r}") from e