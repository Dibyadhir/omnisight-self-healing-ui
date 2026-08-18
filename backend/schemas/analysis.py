from pydantic import BaseModel, model_validator


class AnalyzeRequest(BaseModel):
    screenshot: str | None = None
    dom: str | None = None

    @model_validator(mode="after")
    def validate_analysis_input(self):
        if not self.screenshot and not self.dom:
            raise ValueError("At least screenshot or DOM must be provided")
        return self


class AnalyzeResponse(BaseModel):
    status: str
    message: str
    screenshot_received: bool
    dom_received: bool
    analysis: str