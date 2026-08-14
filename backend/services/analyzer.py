def analyze_ui(screenshot: str | None, dom: str | None) -> dict:
    """
    Analyze the provided UI screenshot and DOM data.
    """

    result = {
        "screenshot_received": screenshot is not None,
        "dom_received": dom is not None,
    }

    return result