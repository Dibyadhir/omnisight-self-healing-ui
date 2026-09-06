from pathlib import Path


def apply_css_fix(
    html_file: str,
    css_code: str
) -> bool:
    """
    Apply generated CSS code to a local HTML file.
    """

    if not css_code:
        return False

    html_path = Path(html_file)

    if not html_path.exists():
        return False

    html_content = html_path.read_text(
        encoding="utf-8"
    )

    style_tag = f"""
<style id="omnisight-ai-fix">
{css_code}
</style>
"""

    # Remove previously generated AI fix
    start_marker = '<style id="omnisight-ai-fix">'
    end_marker = "</style>"

    if start_marker in html_content:
        start = html_content.index(start_marker)
        end = html_content.index(
            end_marker,
            start
        ) + len(end_marker)

        html_content = (
            html_content[:start]
            + html_content[end:]
        )

    # Add the new AI-generated CSS before </head>
    if "</head>" in html_content:
        html_content = html_content.replace(
            "</head>",
            style_tag + "\n</head>",
            1
        )
    else:
        return False

    html_path.write_text(
        html_content,
        encoding="utf-8"
    )

    return True