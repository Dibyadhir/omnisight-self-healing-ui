import re


def validate_css(css_code: str) -> dict:
    """
    Validate AI-generated CSS before applying it.
    """

    if not css_code or not css_code.strip():
        return {
            "valid": False,
            "message": "No CSS code provided"
        }

    css = css_code.strip()

    # Reject HTML
    if re.search(r"<\s*(html|body|div|button|script|style|input|form)", css, re.IGNORECASE):
        return {
            "valid": False,
            "message": "HTML code detected"
        }

    # Reject JavaScript
    if re.search(r"\b(function|const|let|var|document\.|window\.)\b", css):
        return {
            "valid": False,
            "message": "JavaScript code detected"
        }

    # Reject Markdown code fences
    if "```" in css:
        return {
            "valid": False,
            "message": "Markdown code fence detected"
        }

    # Basic CSS brace validation
    if css.count("{") != css.count("}"):
        return {
            "valid": False,
            "message": "Unbalanced CSS braces"
        }

    # CSS should contain a selector block
    if "{" not in css or "}" not in css:
        return {
            "valid": False,
            "message": "Invalid CSS structure"
        }

    return {
        "valid": True,
        "message": "CSS validation successful",
        "css": css
    }