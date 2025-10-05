import os

# Custom exception for path normalization errors
class PathCheckError(Exception):
    pass

def normalize_paths(working_directory, target_path):
    try:
        # Resolve both working directory and target path to absolute, real paths
        working_path = os.path.realpath(os.path.abspath(working_directory))
        full_path = os.path.realpath(os.path.abspath(os.path.join(working_directory, target_path)))
        # Return both paths for further security checks
        return working_path, full_path
    except ValueError as e:
        # Raise a specific error if base and target are on different filesystem roots, e.g. different drives on Windows
        raise PathCheckError(f"base and target are on different roots: base={working_directory!r}, target={target_path!r}") from e
    except Exception as e:
        # Raise a generic runtime error for any other path issues
        raise RuntimeError(f"path check failed for base={working_directory!r}, target={target_path!r}") from e