import requests


OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL_NAME = "llava:7b"


def analyze_with_vlm(
    screenshot: str | None,
    dom: str | None
) -> dict:
    """
    Analyze UI screenshot and DOM using local LLaVA VLM through Ollama.
    """

    prompt = f"""
You are an expert UI/UX QA engineer.

Analyze the provided UI screenshot together with the raw HTML/DOM.

Identify:
1. Visual layout issues
2. Broken or missing UI elements
3. Overlapping elements
4. Alignment or spacing problems
5. Responsive/mobile viewport issues
6. Differences between the screenshot and DOM structure

For every detected issue, provide:
- issue type
- affected element
- severity
- clear description
- suggested CSS or React fix

If no clear visual issue is detected, say so.

Raw HTML/DOM:
{dom if dom else "No DOM provided"}

Return a concise and actionable UI QA analysis.
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
        "stream": False
    }

    try:
        response = requests.post(
            OLLAMA_URL,
            json=payload,
            timeout=600
        )

        response.raise_for_status()

        data = response.json()

        analysis = data["message"]["content"]

        return {
            "analysis": analysis,
            "screenshot_received": screenshot is not None,
            "dom_received": dom is not None,
        }

    except requests.RequestException as error:
        return {
            "analysis": f"VLM service error: {error}",
            "screenshot_received": screenshot is not None,
            "dom_received": dom is not None,
        }
