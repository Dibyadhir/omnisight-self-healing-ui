import re


def extract_code_blocks(vlm_response: str) -> list[dict]:
    """
    Extract executable code blocks from a VLM response.
    """

    if not vlm_response:
        return []

    pattern = r"```(?:([a-zA-Z0-9_+-]+))?\s*(.*?)```"

    matches = re.findall(
        pattern,
        vlm_response,
        re.DOTALL
    )

    code_blocks = []

    for language, code in matches:
        code_blocks.append({
            "language": language.lower() if language else "unknown",
            "code": code.strip()
        })

    return code_blocks