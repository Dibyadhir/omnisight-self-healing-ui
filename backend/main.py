from fastapi import FastAPI

app = FastAPI(title="OmniSight API")


@app.get("/")
def home():
    return {"message": "OmniSight API is running"}


@app.get("/health")
def health():
    return {"status": "healthy"}