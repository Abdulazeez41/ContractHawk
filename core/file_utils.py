import os
from pathlib import Path

def normalize_path(path: str) -> str:
    return os.path.abspath(Path(path).expanduser())

