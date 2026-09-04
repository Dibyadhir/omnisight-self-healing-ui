"""
OmniSight - Week 2: Multimodal Prompting (Gemini version)
--------------------------------------------------------------
Sends a screenshot (captured by Week 1's automation) to Google's Gemini
model and asks it to act as an autonomous QA engineer, spotting visual
anomalies like overlapping text, clipping elements, or bad contrast.
Requirements:
    pip install google-genai
Environment variable required:
    GEMINI_API_KEY  (set this before running - see setup instructions)
Run with:
    python analyze_screenshot_gemini.py
"""

import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Loads variables from a .env file in the same folder into the environment
load_dotenv()

SCREENSHOT_PATH = "screenshots/checkout-overview-BUGGED.png"
MODEL = "gemini-3.6-flash"

SYSTEM_PROMPT = """You are an autonomous QA engineer reviewing a screenshot of a
web application's checkout page. Your job is to identify visual bugs that a
human tester would flag - NOT to describe the page in general.

Look specifically for:
- Text or buttons that overlap or clip outside the visible viewport
- Elements with poor contrast that would be hard to read
- Misaligned or overlapping UI components
- Anything that looks broken or unintentional given this is a mobile viewport

If you find an issue, describe:
1. What the issue is
2. Where it is on the page
3. A specific, actionable fix (e.g. suggested CSS change)

If the page looks correct with no visual bugs, say so clearly - do not
invent problems that aren't there."""

def main():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError(
            "GEMINI_API_KEY environment variable not set. "
            "See setup instructions before running this script."
        )

    if not os.path.exists(SCREENSHOT_PATH):
        raise FileNotFoundError(
            f"Screenshot not found at '{SCREENSHOT_PATH}'. "
            "Update SCREENSHOT_PATH to point at a real file from your "
            "screenshots/ folder generated in Week 1."
        )

    client = genai.Client(api_key=api_key)

    print(f"Reading image: {SCREENSHOT_PATH}")
    with open(SCREENSHOT_PATH, "rb") as f:
        image_bytes = f.read()

    print(f"Sending to {MODEL} for visual QA review...\n")

    response = client.models.generate_content(
        model=MODEL,
        contents=[
            types.Part.from_bytes(data=image_bytes, mime_type="image/png"),
            "Review this checkout page screenshot for visual bugs.",
        ],
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
            max_output_tokens=2048,
        ),
    )

    result_text = response.text

    print("=" * 60)
    print("VLM QA REVIEW RESULT")
    print("=" * 60)
    print(result_text)

    os.makedirs("output", exist_ok=True)
    with open("output/vlm_review.txt", "w", encoding="utf-8") as f:
        f.write(result_text)
    print("\nSaved full result to output/vlm_review.txt")

if __name__ == "__main__":
    main()