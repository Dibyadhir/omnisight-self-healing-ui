import re
import requests


OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL_NAME = "llava:7b"


def clean_css(raw_fix):
    """
    Clean LLM/RAG output and extract only CSS code.
    """

    if not raw_fix:
        return ""

    raw_fix = raw_fix.strip()

    # If response contains Markdown code fence
    match = re.search(
        r"```(?:css)?\s*(.*?)```",
        raw_fix,
        re.DOTALL | re.IGNORECASE
    )

    if match:
        raw_fix = match.group(1).strip()

    return raw_fix


def generate_fix(issue, rag_matches):
    """
    Generate a safe CSS fix.

    If RAG has a strong matching example, use it directly.
    Otherwise generate a new fix using LLaVA.
    """

    # -------------------------------------------------
    # STEP 1: Check RAG for a strong matching solution
    # -------------------------------------------------

    if rag_matches:

        best_match = rag_matches[0]

        score = best_match.get("score", 0)
        rag_example = best_match.get("example", "")

        # Strong RAG match
        if score >= 4 and rag_example:

            clean_fix = clean_css(rag_example)

            return {
                "status": "success",
                "fix": clean_fix,
                "source": "rag"
            }

    # -------------------------------------------------
    # STEP 2: No strong RAG match → use LLaVA
    # -------------------------------------------------

    rag_text = ""

    for match in rag_matches[:1]:
        rag_text += f"""
Problem: {match.get('problem', '')}
Solution: {match.get('solution', '')}
Fix Type: {match.get('fix_type', '')}
Example: {match.get('example', '')}
"""

    prompt = f"""
You are an expert frontend developer.

Generate a safe CSS fix ONLY for this UI issue.

UI Issue:
{issue.get('description', '')}

Affected Element:
{issue.get('affected_element', '')}

Severity:
{issue.get('severity', '')}

Relevant RAG knowledge:
{rag_text}

Rules:
- Generate ONLY CSS.
- Fix ONLY the specified issue.
- Do not fix other issues.
- Do not modify HTML.
- Do not modify JavaScript.
- Keep the fix minimal.
- Do not repeat selectors unnecessarily.
- Do not explain anything.
- Do not use Markdown.
- Do not use code fences.

Return only CSS code.
"""

    payload = {
        "model": MODEL_NAME,
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "stream": False
    }

    try:

        response = requests.post(
            OLLAMA_URL,
            json=payload,
            timeout=300
        )

        response.raise_for_status()

        data = response.json()

        raw_fix = data["message"]["content"].strip()

        clean_fix = clean_css(raw_fix)

        return {
            "status": "success",
            "fix": clean_fix,
            "source": "llm"
        }

    except Exception as error:

        return {
            "status": "error",
            "fix": "",
            "source": "llm",
            "message": str(error)
        }