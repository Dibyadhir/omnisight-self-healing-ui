import re
from pathlib import Path


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


def apply_css_fix(
    css_file: str,
    css_code: str,
    backup: bool = True
) -> dict:
    """
    Safely apply AI-generated CSS code to a CSS file.
    """

    if not css_code or not css_code.strip():
        return {
            "success": False,
            "message": "No CSS code provided"
        }

    css_path = Path(css_file)

    if not css_path.exists():
        return {
            "success": False,
            "message": f"CSS file not found: {css_file}"
        }

    try:
        # Create backup before modifying the file
        if backup:
            backup_path = css_path.with_suffix(".css.backup")

            if not backup_path.exists():
                backup_path.write_text(
                    css_path.read_text(encoding="utf-8"),
                    encoding="utf-8"
                )

        # Read existing CSS
        existing_css = css_path.read_text(
            encoding="utf-8"
        )

        # Add AI-generated fix
        updated_css = (
            existing_css
            + "\n\n"
            + "/* ==========================\n"
              "   OmniSight AI Generated Fix\n"
              "========================== */\n\n"
            + css_code.strip()
            + "\n"
        )

        css_path.write_text(
            updated_css,
            encoding="utf-8"
        )

        return {
            "success": True,
            "message": "CSS fix applied successfully",
            "file": str(css_path)
        }

    except Exception as e:
        return {
            "success": False,
            "message": str(e)
        }