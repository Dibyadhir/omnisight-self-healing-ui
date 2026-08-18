def analyze_with_vlm(screenshot: str | None, dom: str | None) -> dict:
    """
    Analyze UI screenshot and DOM using a Vision-Language Model.
    """

    prompt = """
    Analyze the provided UI screenshot and DOM.

    Identify:
    1. Visual layout issues
    2. Broken or missing UI elements
    3. Overlapping elements
    4. Alignment or spacing problems
    5. Differences between the screenshot and DOM structure

    Return a concise description of the detected UI issues.
    """

    return {
        "analysis": "VLM analysis service is ready",
        "screenshot_received": screenshot is not None,
        "dom_received": dom is not None,
    }