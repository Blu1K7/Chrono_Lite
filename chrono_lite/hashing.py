"""
Chrono_Lite hashing utilities.

Provides a minimal, tamper-aware hashing workflow for images and videos.
Uses SHA-256 as the canonical hashing method.
"""

import hashlib
from pathlib import Path


def sha256_file(filepath: str) -> str:
    """
    Computes SHA-256 hash of a file in streaming mode (memory efficient).

    Args:
        filepath (str): Path to the file.

    Returns:
        str: Hexadecimal SHA-256 hash string.
    """
    path = Path(filepath)

    if not path.exists():
        raise FileNotFoundError(f"File not found: {filepath}")

    hash_sha256 = hashlib.sha256()

    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            hash_sha256.update(chunk)

    return hash_sha256.hexdigest()


__all__ = [
    "sha256_file",
]
