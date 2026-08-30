import requests


OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL_NAME = "llava:7b"


def analyze_with_vlm(
    screenshot: str | None,
    dom: str | None
) -> dict:
    """
    Analyze UI screenshot and DOM using local LLaVA VLM through Ollama.
    Returns structured JSON-compatible UI issues.
    """

    # Limit DOM size to avoid context overflow
    dom_text = dom[:2000] if dom else "No DOM provided"

    prompt = f"""
You are an expert UI/UX QA engineer.

Analyze the provided UI screenshot together with the HTML DOM.

Focus ONLY on clearly visible UI problems.

Look for:
1. Visual layout issues
2. Broken or missing UI elements
3. Overlapping elements
4. Alignment or spacing problems
5. Responsive/mobile viewport issues
6. Overflow or clipping
7. Invisible or unreadable text

For every detected issue, identify:
- issue_type
- affected_element
- severity
- description
- css_fix

IMPORTANT:
Return ONLY valid JSON.
Do not write explanations before or after the JSON.
Do not use Markdown.
Do not use ```json code fences.

Use EXACTLY this format:

{{
  "issues": [
    {{
      "issue_type": "string",
      "affected_element": "string",
      "severity": "low|medium|high",
      "description": "string",
      "css_fix": "string"
    }}
  ]
}}

If no clear issue is detected, return:

{{
  "issues": []
}}

HTML/DOM:
{dom_text}
"""

    payload = {
        "model": MODEL_NAME,
        "messages": [
            {
                "role": "user",
                "content": prompt,
                "images": [screenshot] if screenshot else []
            }
        ],
        "stream": False,
        "format": "json",
        "options": {
            "num_ctx": 4096,
            "num_predict": 300
        }
    }

    try:
        response = requests.post(
            OLLAMA_URL,
            json=payload,
            timeout=900
        )

        print("OLLAMA STATUS:", response.status_code)

        response.raise_for_status()

        data = response.json()

        analysis = data["message"]["content"]

        return {
            "status": "success",
            "analysis": analysis,
            "screenshot_received": screenshot is not None,
            "dom_received": dom is not None,
        }

    except requests.RequestException as error:
        return {
            "status": "error",
            "analysis": f"VLM service error: {error}",
            "screenshot_received": screenshot is not None,
            "dom_received": dom is not None,
        }

    except (KeyError, TypeError, ValueError) as error:
        return {
            "status": "error",
            "analysis": f"Invalid VLM response: {error}",
            "screenshot_received": screenshot is not None,
            "dom_received": dom is not None,
        }