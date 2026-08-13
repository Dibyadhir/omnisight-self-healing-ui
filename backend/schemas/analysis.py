from pydantic import BaseModel


class AnalyzeRequest(BaseModel):
    screenshot: str | None = None
    dom: str | None = None


class AnalyzeResponse(BaseModel):
    status: str
    message: str