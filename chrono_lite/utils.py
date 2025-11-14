# utils.py — ChronoLite Utility Module

def safe_int(value, default=0):
    try:
        return int(value)
    except (ValueError, TypeError):
        return default


def format_timestamp(ts):
    """Format timestamp into a human-readable string."""
    import datetime
    return datetime.datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S")


def debug(message):
    """Simple debug print hook."""
    print(f"[CHRONOLITE DEBUG] {message}")
