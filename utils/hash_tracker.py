import os
import json
import hashlib
from typing import Dict

HASHES_FILE = "cache/hashes.json"

def compute_file_hash(path: str) -> str:
    sha256 = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(8192):
            sha256.update(chunk)
    return sha256.hexdigest()

def load_hash_cache() -> Dict[str, str]:
    if not os.path.exists(HASHES_FILE):
        return {}
    with open(HASHES_FILE, "r") as f:
        return json.load(f)

def save_hash_cache(cache: Dict[str, str]) -> None:
    os.makedirs(os.path.dirname(HASHES_FILE), exist_ok=True)
    with open(HASHES_FILE, "w") as f:
        json.dump(cache, f, indent=2)

def has_changed(file_path: str, cache: Dict[str, str]) -> bool:
    new_hash = compute_file_hash(file_path)
    old_hash = cache.get(file_path)
    return new_hash != old_hash

def update_hash(file_path: str, cache: Dict[str, str]) -> None:
    cache[file_path] = compute_file_hash(file_path)
