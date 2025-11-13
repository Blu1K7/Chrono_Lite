"""
Metadata parser for Chrono_Lite.
Provides lightweight extraction of EXIF, XMP and video timestamps.
"""

from datetime import datetime
from PIL import Image
from PIL.ExifTags import TAGS
import subprocess
import json
import os


def extract_exif_timestamp(image_path: str):
    """Extract EXIF timestamp from an image file."""
    try:
        img = Image.open(image_path)
        exif = img.getexif()

        for tag_id, value in exif.items():
            tag = TAGS.get(tag_id, tag_id)
            if tag == "DateTimeOriginal":
                return value

        return None

    except Exception:
        return None


def extract_xmp_timestamp(image_path: str):
    """Extracts XMP timestamp if present (very lightweight scan)."""
    try:
        with open(image_path, "rb") as f:
            data = f.read().decode("latin-1", errors="ignore")

        if "<xmp:CreateDate>" in data:
            start = data.index("<xmp:CreateDate>") + len("<xmp:CreateDate>")
            end = data.index("</xmp:CreateDate>")
            return data[start:end].strip()

        return None

    except Exception:
        return None


def extract_video_timestamp(video_path: str):
    """Extract creation timestamp from a video using ffprobe."""
    try:
        cmd = [
            "ffprobe", "-v", "quiet", "-print_format", "json",
            "-show_entries", "format_tags=creation_time",
            video_path
        ]

        out = subprocess.check_output(cmd).decode("utf-8")
        meta = json.loads(out)

        if "format" in meta and "tags" in meta["format"]:
            return meta["format"]["tags"].get("creation_time")

        return None

    except Exception:
        return None


def extract_all_timestamps(path: str):
    """Unified extraction wrapper."""
    if not os.path.exists(path):
        raise FileNotFoundError("File not found")

    timestamps = {
        "exif": extract_exif_timestamp(path),
        "xmp": extract_xmp_timestamp(path),
        "video": extract_video_timestamp(path)
    }

    # Pick first non-null timestamp
    canonical = next((t for t in timestamps.values() if t), None)
    return canonical, timestamps
