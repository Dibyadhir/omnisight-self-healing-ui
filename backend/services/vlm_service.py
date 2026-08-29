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

    # Keep DOM small so LLaVA has enough context for the screenshot.
    dom_text = dom[:2000] if dom else "No DOM provided"

    prompt = f"""
You are a UI/UX QA engineer.

Analyze the screenshot and the HTML DOM.

Find only clearly visible UI problems.

Focus on:
- invisible or unreadable elements
- broken buttons
- overflow or clipping
- alignment and spacing
- responsive/mobile issues

For each issue provide:
- issue type
- affected element
- severity
- description
- CSS fix

Do not invent problems.

DOM:
{dom_text}

Return a short actionable UI QA analysis.
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