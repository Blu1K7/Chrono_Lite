"""
Core timestamp extraction logic for Chrono_Lite.

This module provides a minimal, dependency-free way to extract:
- EXIF timestamps (when available)
- XMP timestamps (basic parsing)
- Filesystem timestamps (ultimate fallback)

Designed for lightweight OSINT workflows.
"""

import os
import re
from datetime import datetime

# --- Timestamp utilities -----------------------------------------------------

EXIF_KEYS = [
    "DateTimeOriginal",
    "CreateDate",
    "ModifyDate",
]

XMP_REGEX = re.compile(
    rb"<xmp:CreateDate>(.*?)</xmp:CreateDate>|"
    rb"<xmp:ModifyDate>(.*?)</xmp:ModifyDate>",
    re.IGNORECASE,
)

def _normalize(ts: str) -> str:
    """Normalize timestamps to ISO-8601 when possible."""
    ts = ts.strip().replace(":", "-", 2)
    try:
        return datetime.fromisoformat(ts).isoformat()
    except Exception:
        return ts  # return raw if normalization impossible

# --- EXIF parsing ------------------------------------------------------------

def extract_exif(path: str) -> str | None:
    """Extract creation timestamps from binary EXIF headers."""
    try:
        with open(path, "rb") as f:
            data = f.read()
    except Exception:
        return None

    for key in EXIF_KEYS:
        if key.encode() in data:
            # find "Key\x00VALUE\x00"
            idx = data.find(key.encode())
            segment = data[idx:idx + 40]  # small window
            parts = re.findall(rb"\d{4}:\d{2}:\d{2} \d{2}:\d{2}:\d{2}", segment)
            if parts:
                return _normalize(parts[0].decode())

    return None

# --- XMP parsing -------------------------------------------------------------

def extract_xmp(path: str) -> str | None:
    """Lightweight XMP timestamp extraction."""
    try:
        with open(path, "rb") as f:
            data = f.read()
    except Exception:
        return None

    match = XMP_REGEX.search(data)
    if not match:
        return None

    for group in match.groups():
        if group:
            return _normalize(group.decode())

    return None

# --- Filesystem fallback -----------------------------------------------------

def extract_fs(path: str) -> str:
    """Fallback: filesystem creation or modification time."""
    stat = os.stat(path)
    timestamp = stat.st_mtime
    return datetime.fromtimestamp(timestamp).isoformat()

# --- Public API --------------------------------------------------------------

def extract_timestamp(path: str) -> dict:
    """
    Unified timestamp extraction workflow.

    Returns:
        {
            "source": "exif" | "xmp" | "filesystem",
            "timestamp": "<ISO8601 string>"
        }
    """
    exif = extract_exif(path)
    if exif:
        return {"source": "exif", "timestamp": exif}

    xmp = extract_xmp(path)
    if xmp:
        return {"source": "xmp", "timestamp": xmp}

    return {"source": "filesystem", "timestamp": extract_fs(path)}
