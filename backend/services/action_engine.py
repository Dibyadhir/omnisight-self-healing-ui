import re
from pathlib import Path

from backend.services.css_validator import validate_css


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
    Apply validated CSS code to a CSS file.
    """

    # -----------------------------
    # STEP 1: Validate CSS
    # -----------------------------

    validation = validate_css(css_code)

    if not validation["valid"]:
        return {
            "success": False,
            "message": f"CSS validation failed: {validation['message']}"
        }

    clean_css = validation["css"]

    # -----------------------------
    # STEP 2: Check CSS file
    # -----------------------------

    css_path = Path(css_file)

    if not css_path.exists():
        return {
            "success": False,
            "message": f"CSS file not found: {css_file}"
        }

    try:

        # -----------------------------
        # STEP 3: Create backup
        # -----------------------------

        if backup:

            backup_path = css_path.with_suffix(".css.backup")

            if not backup_path.exists():

                backup_path.write_text(
                    css_path.read_text(encoding="utf-8"),
                    encoding="utf-8"
                )

        # -----------------------------
        # STEP 4: Read existing CSS
        # -----------------------------

        existing_css = css_path.read_text(
            encoding="utf-8"
        )

        # -----------------------------
        # STEP 5: Apply CSS
        # -----------------------------

        updated_css = (
            existing_css
            + "\n\n"
            + "/* ==========================\n"
              "   OmniSight AI Generated Fix\n"
              "========================== */\n\n"
            + clean_css
            + "\n"
        )

        css_path.write_text(
            updated_css,
            encoding="utf-8"
        )

        return {
            "success": True,
            "message": "Validated CSS fix applied successfully",
            "file": str(css_path),
            "validation": validation
        }

    except Exception as error:

        return {
            "success": False,
            "message": str(error)
        }