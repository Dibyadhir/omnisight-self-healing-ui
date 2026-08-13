from fastapi import APIRouter
from backend.schemas.analysis import AnalyzeRequest, AnalyzeResponse


router = APIRouter(prefix="/api", tags=["Analysis"])


@router.post("/analyze", response_model=AnalyzeResponse)
def analyze(request: AnalyzeRequest):
    return AnalyzeResponse(
        status="success",
        message="Analysis request received"
    )