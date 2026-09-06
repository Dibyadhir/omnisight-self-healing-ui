from fastapi import APIRouter
from backend.schemas.webhook import WebhookRequest, WebhookResponse


router = APIRouter(prefix="/api", tags=["Webhook"])


@router.post("/webhook", response_model=WebhookResponse)
def receive_webhook(request: WebhookRequest):
    return WebhookResponse(
        status="received",
        message=f"Build event received: {request.event}",
        build_id=request.build_id
    )