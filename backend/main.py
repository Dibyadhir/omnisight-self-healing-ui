from fastapi import FastAPI
from backend.routes.analysis import router as analysis_router

app = FastAPI(title="OmniSight API")

app.include_router(analysis_router)

@app.get("/")
def home():
    return {"message": "OmniSight API is running"}


@app.get("/health")
def health():
    return {"status": "healthy"}