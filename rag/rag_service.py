import json
from pathlib import Path

KNOWLEDGE_BASE = Path(__file__).parent / "knowledge" / "ui_fixes.json"


def load_knowledge_base():
    with open(KNOWLEDGE_BASE, "r", encoding="utf-8") as file:
        return json.load(file)


def search_knowledge(problem: str, top_k: int = 3):
    if not problem:
        return []

    problem_words = set(problem.lower().split())
    knowledge = load_knowledge_base()
    results = []

    for item in knowledge:
        text = (
            item["problem"]
            + " "
            + item["solution"]
            + " "
            + item.get("fix_type", "")
        ).lower()

        text_words = set(text.split())
        score = len(problem_words & text_words)

        if score > 0:
            results.append({
                "score": score,
                "problem": item["problem"],
                "solution": item["solution"],
                "fix_type": item["fix_type"],
                "example": item.get("example", "")
            })

    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:top_k]