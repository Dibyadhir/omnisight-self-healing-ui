import base64

from backend.services.langchain_service import analyze_with_langchain


SCREENSHOT_PATH = "screenshots/checkout-overview-BUGGED.png"
DOM_PATH = "dom_snapshots/checkout-overview-BUGGED.html"


def main():
    with open(SCREENSHOT_PATH, "rb") as image_file:
        screenshot = base64.b64encode(image_file.read()).decode("utf-8")

    with open(DOM_PATH, "r", encoding="utf-8") as dom_file:
        dom = dom_file.read()

    print("Sending BUGGED screenshot + DOM to LangChain/LLaVA...")
    print("Please wait...\n")

    result = analyze_with_langchain(
        screenshot=screenshot,
        dom=dom
    )

    print("========== VLM ANALYSIS ==========\n")
    print(result)
    print("\n========== END ANALYSIS ==========")


if __name__ == "__main__":
    main()