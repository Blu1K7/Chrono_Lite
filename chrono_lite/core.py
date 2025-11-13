"""
Core processing module for Chrono_Lite.

Houses the main interface used by analysts for timestamp extraction
and integrity validation.
"""

from .parser import extract_timestamps
from .hashing import compute_sha256


def analyze_media(path: str) -> dict:
    """
    High-level unified analysis function.
    
    Returns:
        {
            "timestamps": {...},
            "hash": "..."
        }
    """
    timestamps = extract_timestamps(path)
    digest = compute_sha256(path)

    return {
        "timestamps": timestamps,
        "hash": digest
    }
