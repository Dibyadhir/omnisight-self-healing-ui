import json

from backend.services.analyzer import analyze_ui
from backend.services.rag_integration import get_rag_context_from_vlm
from backend.services.fix_generator import generate_fix
from backend.services.action_engine import apply_css_fix


def run_self_healing(
    screenshot: str | None,
    dom: str | None,
    css_file: str
) -> dict:
    """
    Complete OmniSight self-healing pipeline.

    Flow:
    Screenshot + DOM
        ↓
    VLM Analysis
        ↓
    RAG
        ↓
    Fix Generator
        ↓
    CSS Validator + Action Engine
    """

    # -----------------------------------------
    # STEP 1: VLM ANALYSIS
    # -----------------------------------------

    vlm_result = analyze_ui(
        screenshot=screenshot,
        dom=dom
    )

    if vlm_result.get("status") != "success":
        return {
            "status": "error",
            "step": "vlm",
            "message": vlm_result.get("analysis", "VLM analysis failed")
        }

    vlm_analysis = vlm_result.get("analysis", "")

    # -----------------------------------------
    # STEP 2: PARSE VLM RESPONSE
    # -----------------------------------------

    try:
        parsed_analysis = json.loads(vlm_analysis)
    except json.JSONDecodeError:
        return {
            "status": "error",
            "step": "vlm_parse",
            "message": "VLM returned invalid JSON",
            "raw_analysis": vlm_analysis
        }

    issues = parsed_analysis.get("issues", [])

    if not issues:
        return {
            "status": "success",
            "message": "No UI issues detected",
            "issues": [],
            "fixes": []
        }

    # -----------------------------------------
    # STEP 3: RAG
    # -----------------------------------------

    rag_results = get_rag_context_from_vlm(vlm_analysis)

    fixes = []

    # -----------------------------------------
    # STEP 4: GENERATE + APPLY FIXES
    # -----------------------------------------

    for item in rag_results:

        issue = item.get("issue", {})
        rag_matches = item.get("rag_matches", [])

        fix_result = generate_fix(
            issue,
            rag_matches
        )

        if fix_result.get("status") != "success":
            fixes.append({
                "issue": issue,
                "status": "failed",
                "message": fix_result.get(
                    "message",
                    "Fix generation failed"
                )
            })
            continue

        css_fix = fix_result.get("fix", "")

        if not css_fix:
            fixes.append({
                "issue": issue,
                "status": "failed",
                "message": "No CSS fix generated"
            })
            continue

        # -----------------------------------------
        # STEP 5: ACTION ENGINE
        # -----------------------------------------

        action_result = apply_css_fix(
            css_file=css_file,
            css_code=css_fix,
            backup=True
        )

        fixes.append({
            "issue": issue,
            "fix": css_fix,
            "fix_source": fix_result.get("source"),
            "action": action_result
        })

    # -----------------------------------------
    # FINAL RESULT
    # -----------------------------------------

    return {
        "status": "success",
        "message": "Self-healing pipeline completed",
        "issues": issues,
        "fixes": fixes
    }