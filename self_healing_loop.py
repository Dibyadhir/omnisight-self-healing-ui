"""
OmniSight - Week 3: The Self-Healing Loop
---------------------------------------------
Implements the full "Plan -> Execute -> Evaluate" agentic loop:

  1. PLAN:    Inject a deliberate bug, screenshot it, ask Gemini to
              diagnose it and suggest a CSS fix.
  2. EXECUTE: Extract the CSS from Gemini's response and apply it
              live to the page.
  3. EVALUATE: Take a new screenshot and ask Gemini to verify whether
              the bug is actually fixed. If not, retry (up to a
              maximum number of attempts).

Requirements:
    pip install playwright google-genai python-dotenv
    playwright install chromium

Run with:
    python self_healing_loop.py
"""

import os
import re
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright, Page
from google import genai
from google.genai import types

load_dotenv()


BASE_URL = "http://localhost:5173"
USERNAME = "standard_user"
PASSWORD = "secret_sauce"

MODEL = "gemini-3.6-flash"
MAX_ATTEMPTS = 3  # how many times the loop will retry before giving up

SCREENSHOT_DIR = "screenshots/self_healing"
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

# The same deliberate bugs from Week 2, so we have a known problem to solve
BUGGY_CSS = """
#finish {
  color: #ffffff !important;
  background-color: #ffffff !important;
  border: none !important;
}
.summary_total_label {
  margin-left: -600px !important;
}
"""

DIAGNOSE_PROMPT = """You are an autonomous QA engineer. You are given a
screenshot of a checkout page and its HTML. Cross-reference them to find
visual bugs (elements that exist in the HTML but are not visibly usable
due to styling issues).

For each bug found, respond with a short explanation, THEN provide the
exact CSS fix in a single fenced code block like this:

```css
/* your fix here */
```

Only include CSS rules that OVERRIDE the broken styling - assume this CSS
will be injected after the broken styles, so it just needs to win by being
more specific or using !important where needed."""

VERIFY_PROMPT = """You are an autonomous QA engineer verifying a bug fix.
You will see a screenshot of a page AFTER a proposed fix was applied.

Answer with EXACTLY one of these two formats:

PASS: <short explanation of what looks correct now>

or

FAIL: <short explanation of what is still broken>"""


def get_gemini_client():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY not set - check your .env file.")
    return genai.Client(api_key=api_key)


def ask_gemini_to_diagnose(client, screenshot_path, dom_html):
    with open(screenshot_path, "rb") as f:
        image_bytes = f.read()

    response = client.models.generate_content(
        model=MODEL,
        contents=[
            types.Part.from_bytes(data=image_bytes, mime_type="image/png"),
            f"Page HTML:\n```html\n{dom_html[:15000]}\n```",
            "Diagnose the visual bugs and provide a CSS fix.",
        ],
        config=types.GenerateContentConfig(
            system_instruction=DIAGNOSE_PROMPT,
            max_output_tokens=2048,
        ),
    )
    return response.text


def ask_gemini_to_verify(client, screenshot_path):
    with open(screenshot_path, "rb") as f:
        image_bytes = f.read()

    response = client.models.generate_content(
        model=MODEL,
        contents=[
            types.Part.from_bytes(data=image_bytes, mime_type="image/png"),
            "Has the checkout page's bug been fixed? Check that the Finish "
            "button is visible/usable and the order total is visible on screen.",
        ],
        config=types.GenerateContentConfig(
            system_instruction=VERIFY_PROMPT,
            max_output_tokens=300,
        ),
    )
    return response.text


def extract_css(gemini_response_text: str) -> str:
    """Pulls the contents of a ```css ... ``` block out of Gemini's response."""
    match = re.search(r"```css\s*(.*?)```", gemini_response_text, re.DOTALL)
    if not match:
        raise ValueError(
            "Could not find a ```css``` code block in Gemini's response. "
            "Raw response was:\n" + gemini_response_text
        )
    return match.group(1).strip()


# ---------------------------------------------------------------------------
# Playwright helpers
# ---------------------------------------------------------------------------

def navigate_to_broken_checkout(page: Page):
    """Logs in, adds an item, gets to checkout overview, and injects the bug."""
    page.goto(BASE_URL)
    page.fill("#user-name", USERNAME)
    page.fill("#password", PASSWORD)
    page.click("#login-button")
    page.wait_for_selector(".inventory_list")

    page.click(".btn_inventory")
    page.click(".shopping_cart_link")
    page.wait_for_selector(".cart_list")
    page.click("#checkout")
    page.wait_for_selector("#first-name")

    page.fill("#first-name", "Ada")
    page.fill("#last-name", "Lovelace")
    page.fill("#postal-code", "12345")
    page.click("#continue")
    page.wait_for_selector(".summary_info")

    # Inject the deliberate bug
    page.add_style_tag(content=BUGGY_CSS)
    page.wait_for_timeout(300)


# ---------------------------------------------------------------------------
# Main self-healing loop
# ---------------------------------------------------------------------------

def main():
    client = get_gemini_client()

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={"width": 375, "height": 667})
        page = context.new_page()

        print("Setting up broken checkout page...")
        navigate_to_broken_checkout(page)

        broken_screenshot = f"{SCREENSHOT_DIR}/attempt_0_broken.png"
        page.screenshot(path=broken_screenshot, full_page=True)
        dom_html = page.content()
        print(f"Captured broken state: {broken_screenshot}")

        for attempt in range(1, MAX_ATTEMPTS + 1):
            print(f"\n--- PLAN (attempt {attempt}) ---")
            diagnosis = ask_gemini_to_diagnose(client, broken_screenshot, dom_html)
            print(diagnosis)

            try:
                fix_css = extract_css(diagnosis)
            except ValueError as e:
                print(f"Could not extract a fix: {e}")
                break

            print(f"\n--- EXECUTE (attempt {attempt}) ---")
            print("Applying suggested CSS fix:")
            print(fix_css)
            page.add_style_tag(content=fix_css)
            page.wait_for_timeout(300)

            fixed_screenshot = f"{SCREENSHOT_DIR}/attempt_{attempt}_fixed.png"
            page.screenshot(path=fixed_screenshot, full_page=True)

            print(f"\n--- EVALUATE (attempt {attempt}) ---")
            verdict = ask_gemini_to_verify(client, fixed_screenshot)
            print(verdict)

            if verdict.strip().upper().startswith("PASS"):
                print(f"\nSUCCESS after {attempt} attempt(s). Final screenshot: {fixed_screenshot}")
                break
            else:
                print(f"\nAttempt {attempt} did not fully resolve the issue. Retrying...")
                # Update dom_html/broken_screenshot so the next diagnosis
                # attempt reasons about the CURRENT (partially fixed) state
                broken_screenshot = fixed_screenshot
                dom_html = page.content()
        else:
            print(f"\nGave up after {MAX_ATTEMPTS} attempts without a PASS verdict.")

        browser.close()
"""
OmniSight - Week 3: The Self-Healing Loop
---------------------------------------------
Implements the full "Plan -> Execute -> Evaluate" agentic loop:

  1. PLAN:    Inject a deliberate bug, screenshot it, ask Gemini to
              diagnose it and suggest a CSS fix.
  2. EXECUTE: Extract the CSS from Gemini's response and apply it
              live to the page.
  3. EVALUATE: Take a new screenshot and ask Gemini to verify whether
              the bug is actually fixed. If not, retry (up to a
              maximum number of attempts).

Requirements:
    pip install playwright google-genai python-dotenv
    playwright install chromium

Run with:
    python self_healing_loop.py
"""

import os
import re
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright, Page
from google import genai
from google.genai import types

load_dotenv()

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

BASE_URL = "https://www.saucedemo.com"
USERNAME = "standard_user"
PASSWORD = "secret_sauce"

MODEL = "gemini-3.6-flash"
MAX_ATTEMPTS = 3  # how many times the loop will retry before giving up

SCREENSHOT_DIR = "screenshots/self_healing"
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

# The same deliberate bugs from Week 2, so we have a known problem to solve
BUGGY_CSS = """
#finish {
  color: #ffffff !important;
  background-color: #ffffff !important;
  border: none !important;
}
.summary_total_label {
  margin-left: -600px !important;
}
"""

DIAGNOSE_PROMPT = """You are an autonomous QA engineer. You are given a
screenshot of a checkout page and its HTML. Cross-reference them to find
visual bugs (elements that exist in the HTML but are not visibly usable
due to styling issues).

For each bug found, respond with a short explanation, THEN provide the
exact CSS fix in a single fenced code block like this:

```css
/* your fix here */
```

Only include CSS rules that OVERRIDE the broken styling - assume this CSS
will be injected after the broken styles, so it just needs to win by being
more specific or using !important where needed."""

VERIFY_PROMPT = """You are an autonomous QA engineer verifying a bug fix.
You will see a screenshot of a page AFTER a proposed fix was applied.

Answer with EXACTLY one of these two formats:

PASS: <short explanation of what looks correct now>

or

FAIL: <short explanation of what is still broken>"""


# ---------------------------------------------------------------------------
# Gemini helpers
# ---------------------------------------------------------------------------

def get_gemini_client():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY not set - check your .env file.")
    return genai.Client(api_key=api_key)


def ask_gemini_to_diagnose(client, screenshot_path, dom_html):
    with open(screenshot_path, "rb") as f:
        image_bytes = f.read()

    response = client.models.generate_content(
        model=MODEL,
        contents=[
            types.Part.from_bytes(data=image_bytes, mime_type="image/png"),
            f"Page HTML:\n```html\n{dom_html[:15000]}\n```",
            "Diagnose the visual bugs and provide a CSS fix.",
        ],
        config=types.GenerateContentConfig(
            system_instruction=DIAGNOSE_PROMPT,
            max_output_tokens=4096,
            thinking_config=types.ThinkingConfig(
                thinking_level=types.ThinkingLevel.LOW,
            ),
        ),
    )
    return response.text


def ask_gemini_to_verify(client, screenshot_path):
    with open(screenshot_path, "rb") as f:
        image_bytes = f.read()

    response = client.models.generate_content(
        model=MODEL,
        contents=[
            types.Part.from_bytes(data=image_bytes, mime_type="image/png"),
            "Has the checkout page's bug been fixed? Check that the Finish "
            "button is visible/usable and the order total is visible on screen.",
        ],
        config=types.GenerateContentConfig(
            system_instruction=VERIFY_PROMPT,
            max_output_tokens=1024,
            thinking_config=types.ThinkingConfig(
                thinking_level=types.ThinkingLevel.LOW,
            ),
        ),
    )
    return response.text


def extract_css(gemini_response_text: str) -> str:
    """Pulls the contents of a ```css ... ``` block out of Gemini's response."""
    match = re.search(r"```css\s*(.*?)```", gemini_response_text, re.DOTALL)
    if not match:
        raise ValueError(
            "Could not find a ```css``` code block in Gemini's response. "
            "Raw response was:\n" + gemini_response_text
        )
    return match.group(1).strip()


# ---------------------------------------------------------------------------
# Playwright helpers
# ---------------------------------------------------------------------------

def navigate_to_broken_checkout(page: Page):
    """Logs in, adds an item, gets to checkout overview, and injects the bug."""
    page.goto(BASE_URL)
    page.fill("#user-name", USERNAME)
    page.fill("#password", PASSWORD)
    page.click("#login-button")
    page.wait_for_selector(".inventory_list")

    page.click(".btn_inventory")
    page.click(".shopping_cart_link")
    page.wait_for_selector(".cart_list")
    page.click("#checkout")
    page.wait_for_selector("#first-name")

    page.fill("#first-name", "Ada")
    page.fill("#last-name", "Lovelace")
    page.fill("#postal-code", "12345")
    page.click("#continue")
    page.wait_for_selector(".summary_info")

    # Inject the deliberate bug
    page.add_style_tag(content=BUGGY_CSS)
    page.wait_for_timeout(300)


# ---------------------------------------------------------------------------
# Main self-healing loop
# ---------------------------------------------------------------------------

def main():
    client = get_gemini_client()

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={"width": 375, "height": 667})
        page = context.new_page()

        print("Setting up broken checkout page...")
        navigate_to_broken_checkout(page)

        broken_screenshot = f"{SCREENSHOT_DIR}/attempt_0_broken.png"
        page.screenshot(path=broken_screenshot, full_page=True)
        dom_html = page.content()
        print(f"Captured broken state: {broken_screenshot}")

        for attempt in range(1, MAX_ATTEMPTS + 1):
            print(f"\n--- PLAN (attempt {attempt}) ---")
            diagnosis = ask_gemini_to_diagnose(client, broken_screenshot, dom_html)
            print(diagnosis)

            try:
                fix_css = extract_css(diagnosis)
            except ValueError as e:
                print(f"Could not extract a fix: {e}")
                break

            print(f"\n--- EXECUTE (attempt {attempt}) ---")
            print("Applying suggested CSS fix:")
            print(fix_css)
            page.add_style_tag(content=fix_css)
            page.wait_for_timeout(300)

            fixed_screenshot = f"{SCREENSHOT_DIR}/attempt_{attempt}_fixed.png"
            page.screenshot(path=fixed_screenshot, full_page=True)

            print(f"\n--- EVALUATE (attempt {attempt}) ---")
            verdict = ask_gemini_to_verify(client, fixed_screenshot)
            print(verdict)

            if verdict.strip().upper().startswith("PASS"):
                print(f"\nSUCCESS after {attempt} attempt(s). Final screenshot: {fixed_screenshot}")
                break
            else:
                print(f"\nAttempt {attempt} did not fully resolve the issue. Retrying...")
                # Update dom_html/broken_screenshot so the next diagnosis
                # attempt reasons about the CURRENT (partially fixed) state
                broken_screenshot = fixed_screenshot
                dom_html = page.content()
        else:
            print(f"\nGave up after {MAX_ATTEMPTS} attempts without a PASS verdict.")

        browser.close()


if __name__ == "__main__":
    main()

if __name__ == "__main__":
    main()