from backend.services.vlm_service import analyze_with_vlm


def analyze_ui(screenshot: str | None, dom: str | None) -> dict:
    """
    Analyze the provided UI screenshot and DOM data.
    """

    result = analyze_with_vlm(
        screenshot=screenshot,
        dom=dom
    )

    return result