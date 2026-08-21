"""
OmniSight - Week 2 (Upgraded): Multimodal Prompting with Screenshot + DOM
---------------------------------------------------------------------------
Sends BOTH a screenshot AND the page's raw HTML to Gemini together, so the
model can cross-reference what it visually SEES against what actually
EXISTS in the markup.

Why this matters: a screenshot alone can't distinguish "this element
doesn't exist" from "this element exists but is invisible" (e.g. white
text on a white background). Feeding in the HTML closes that gap.

Requirements:
    pip install google-genai python-dotenv

Environment variable required:
    GEMINI_API_KEY  (set this in a .env file in the same folder)

Run with:
    python analyze_with_dom_gemini.py
"""

import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

SCREENSHOT_PATH = "screenshots/checkout-overview-BUGGED.png"
DOM_PATH = "dom_snapshots/checkout-overview-BUGGED.html"

MODEL = "gemini-3.6-flash"

SYSTEM_PROMPT = """You are an autonomous QA engineer reviewing a web page.
You are given TWO things about the SAME page, captured at the same moment:
  1. A screenshot showing what the page visually looks like
  2. The raw HTML (DOM) showing what elements actually exist in the markup

Your job is to cross-reference these two sources to give an ACCURATE diagnosis:

- If an element appears VISUALLY MISSING but DOES exist in the HTML,
  that means it's invisible due to a styling bug (e.g. color matching
  its background, zero opacity, being pushed off-screen with margin/
  position, or being covered by another element) - NOT that it needs
  to be added to the markup.
- If an element is genuinely absent from the HTML, then it truly needs
  to be added.
- Use the actual HTML element IDs, classes, and attributes in your
  answer wherever relevant, so the suggested fix is specific and
  directly actionable.

For each issue found, describe:
1. What the issue is
2. The specific HTML element responsible (id/class from the DOM)
3. Whether this is a "missing element" bug or a "hidden/broken styling"
   bug, and how you determined that from the HTML
4. A specific, actionable CSS/HTML fix

If the page looks correct with no visual bugs, say so clearly - do not
invent problems that aren't there."""


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError(
            "GEMINI_API_KEY environment variable not set. "
            "Make sure your .env file exists and contains it."
        )

    if not os.path.exists(SCREENSHOT_PATH):
        raise FileNotFoundError(f"Screenshot not found at '{SCREENSHOT_PATH}'.")

    if not os.path.exists(DOM_PATH):
        raise FileNotFoundError(
            f"DOM snapshot not found at '{DOM_PATH}'. "
            "Run inject_bug_and_capture.js first to generate it."
        )

    client = genai.Client(api_key=api_key)

    print(f"Reading image: {SCREENSHOT_PATH}")
    with open(SCREENSHOT_PATH, "rb") as f:
        image_bytes = f.read()

    print(f"Reading DOM: {DOM_PATH}")
    with open(DOM_PATH, "r", encoding="utf-8") as f:
        dom_html = f.read()

    # Very simple truncation guard - full pages can be long, and we mainly
    # care about the body content for this kind of visual bug analysis.
    MAX_DOM_CHARS = 15000
    if len(dom_html) > MAX_DOM_CHARS:
        dom_html = dom_html[:MAX_DOM_CHARS] + "\n<!-- ... truncated ... -->"

    print(f"Sending screenshot + DOM to {MODEL} for visual QA review...\n")

    response = client.models.generate_content(
        model=MODEL,
        contents=[
            types.Part.from_bytes(data=image_bytes, mime_type="image/png"),
            f"Here is the page's HTML at the moment this screenshot was taken:\n\n```html\n{dom_html}\n```",
            "Cross-reference the screenshot against this HTML and review the page for visual bugs.",
        ],
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
            max_output_tokens=2048,
        ),
    )

    result_text = response.text

    print("=" * 60)
    print("VLM QA REVIEW RESULT (screenshot + DOM)")
    print("=" * 60)
    print(result_text)

    os.makedirs("output", exist_ok=True)
    with open("output/vlm_review_with_dom.txt", "w", encoding="utf-8") as f:
        f.write(result_text)
    print("\nSaved full result to output/vlm_review_with_dom.txt")


if __name__ == "__main__":
    main()