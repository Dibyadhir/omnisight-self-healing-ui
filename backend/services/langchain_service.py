from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage


MODEL_NAME = "llava:7b"


def analyze_with_langchain(
    screenshot: str | None,
    dom: str | None
) -> str:
    """
    Analyze UI screenshot and DOM using LangChain + local Ollama LLaVA.
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
6. Differences between screenshot and DOM structure

For every detected issue, provide:
- issue type
- affected element
- severity
- clear description
- suggested CSS or React fix

If no clear visual issue is detected, say so.

Raw HTML/DOM:
{dom[:5000] if dom else "No DOM provided"}

Return a concise and actionable UI QA analysis.
"""

    try:
        llm = ChatOllama(
            model=MODEL_NAME,
            base_url="http://localhost:11434",
            temperature=0
        )

        content = [
            {
                "type": "text",
                "text": prompt
            }
        ]

        if screenshot:
            content.append(
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/png;base64,{screenshot}"
                    }
                }
            )

        response = llm.invoke([
            HumanMessage(content=content)
        ])

        return response.content

    except Exception as error:
        return f"LangChain VLM service error: {error}"