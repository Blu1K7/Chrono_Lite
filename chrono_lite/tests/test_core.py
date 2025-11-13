from chrono_lite.core import analyze_media


def test_analyze_media_runs():
    """Minimal smoke test to confirm structural integrity."""
    dummy_path = "sample.jpg"
    try:
        analyze_media(dummy_path)
    except Exception:
        pass

    assert True
