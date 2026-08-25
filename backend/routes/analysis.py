from fastapi import APIRouter
from backend.schemas.analysis import AnalyzeRequest, AnalyzeResponse
from backend.services.analyzer import analyze_ui

router = APIRouter(prefix="/api", tags=["Analysis"])


@router.post("/analyze", response_model=AnalyzeResponse)
def analyze(request: AnalyzeRequest):
    result = analyze_ui(
        screenshot=request.screenshot,
        dom=request.dom
    )


    return AnalyzeResponse(
        status="success",
        message="VLM analysis completed",
        screenshot_received=result["screenshot_received"],
        dom_received=result["dom_received"],
        analysis=result["analysis"]
    )

   
   