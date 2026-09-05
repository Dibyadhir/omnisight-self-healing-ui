from rag.rag_service import search_knowledge


def get_rag_context(vlm_issue: str):
    """
    Get relevant UI fixes from the RAG knowledge base.
    """

    results = search_knowledge(vlm_issue, top_k=3)

    if not results:
        return {
            "issue": vlm_issue,
            "matches": []
        }

    return {
        "issue": vlm_issue,
        "matches": results
    }