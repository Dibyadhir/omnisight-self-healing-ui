from pydantic import BaseModel


class WebhookRequest(BaseModel):
    event: str
    status: str
    build_id: str


class WebhookResponse(BaseModel):
    status: str
    message: str
    build_id: str