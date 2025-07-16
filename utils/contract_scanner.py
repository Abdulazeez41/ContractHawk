import os
from typing import List

def get_all_solidity_files(directory: str) -> List[str]:
    files = []
    for root, _, filenames in os.walk(directory):
        for filename in filenames:
            if filename.endswith(".sol"):
                files.append(os.path.join(root, filename))
    return files
