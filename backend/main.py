from fastapi import FastAPI
from backend.routes.webhook import router as webhook_router


app = FastAPI(title="OmniSight API")

app.include_router(webhook_router)


@app.get("/")
def home():
    return {"message": "OmniSight API is running"}


@app.get("/health")
def health():
    return {"status": "healthy"}