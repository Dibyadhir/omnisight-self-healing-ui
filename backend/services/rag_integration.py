import json

from rag.rag_service import search_knowledge


def get_rag_context(vlm_issue: str):
    """
    Get relevant UI fixes from the RAG knowledge base.
    """

    results = search_knowledge(vlm_issue, top_k=3)

    return {
        "issue": vlm_issue,
        "matches": results
    }


def get_rag_context_from_vlm(vlm_analysis: str):
    """
    Extract issues from VLM JSON response
    and retrieve relevant RAG knowledge.
    """

    if not vlm_analysis:
        return []

    try:
        data = json.loads(vlm_analysis)
    except json.JSONDecodeError:
        return []

    issues = data.get("issues", [])
    results = []

    for issue in issues:
        description = issue.get("description", "")
        affected_element = issue.get("affected_element", "")

        problem = f"{affected_element} {description}".strip()

        if not problem:
            continue

        rag_result = search_knowledge(problem, top_k=3)

        results.append({
            "issue": issue,
            "rag_matches": rag_result
        })

    return results