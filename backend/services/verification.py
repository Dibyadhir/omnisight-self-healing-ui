import json
import re
import requests


OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL_NAME = "llava:7b"


def parse_verification_result(response: str) -> dict:
    """
    Parse and validate the structured verification response
    returned by the VLM.
    """

    if not response:
        return {
            "verified": False,
            "analysis": "Empty verification response."
        }

    cleaned_response = re.sub(
        r"^```(?:json)?\s*|\s*```$",
        "",
        response.strip(),
        flags=re.IGNORECASE
    ).strip()

    try:
        result = json.loads(cleaned_response)

        if not isinstance(result, dict):
            return {
                "verified": False,
                "analysis": "Invalid verification format."
            }

        return {
            "verified": bool(result.get("verified", False)),
            "analysis": str(
                result.get(
                    "analysis",
                    "No verification explanation provided."
                )
            )
        }

    except json.JSONDecodeError:
        return {
            "verified": False,
            "analysis": response
        }


def verify_fix(
    screenshot: str | None,
    dom: str | None
) -> dict:
    """
    Verify whether a previously detected UI issue
    has been resolved using the local VLM.
    """

    prompt = f"""
You are an expert UI/UX verification agent.

A UI fix has already been applied to the webpage.

Analyze the provided screenshot and HTML/DOM and determine
whether the previously detected UI issue has been resolved.

Return ONLY valid JSON:

{{
    "verified": true,
    "analysis": "Brief explanation of the verification result."
}}

Rules:
- Set verified to true only if the UI issue appears fixed.
- Set verified to false if the issue is still present.
- Do not return Markdown.
- Do not return code fences.
- Keep the analysis concise.

HTML/DOM:
{dom if dom else "No DOM provided"}
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

        return parse_verification_result(analysis)

    except requests.RequestException as error:
        return {
            "verified": False,
            "analysis": f"VLM verification error: {error}"
        }

    except (KeyError, TypeError, ValueError) as error:
        return {
            "verified": False,
            "analysis": f"Invalid VLM response: {error}"
        }