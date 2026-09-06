from typing import Literal
from pydantic import BaseModel


class WebhookRequest(BaseModel):
    event: str
    status: Literal["success", "failed"]
    build_id: str


class WebhookResponse(BaseModel):
    status: str
    message: str
    build_id: str