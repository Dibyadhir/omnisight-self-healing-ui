"""
OmniSight - Week 1, Part B: API Scaffolding
---------------------------------------------
A FastAPI server that acts as a webhook receiver for simulated CI/CD
build events (e.g., what GitHub Actions or Jenkins would send when a
build finishes).

Run with:
    python -m uvicorn main:app --reload

Then visit:
    http://127.0.0.1:8000/health        (browser)
    http://127.0.0.1:8000/docs          (interactive API docs - try it here!)
"""

from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

app = FastAPI(title="OmniSight Webhook Gateway")

# In-memory store of received events, just so we can inspect what came in.
# (Week 4 will likely swap this for a real database.)
received_events = []


# ---------------------------------------------------------------------------
# Data model for the incoming webhook payload
# ---------------------------------------------------------------------------
# Pydantic automatically validates incoming JSON against this shape.
# If a request is missing "branch" or sends the wrong type, FastAPI
# rejects it with a clear 422 error before your code even runs.

class CIBuildEvent(BaseModel):
    branch: str
    commit: str
    status: str  # e.g. "success", "failure"
    repository: Optional[str] = None
    staging_url: Optional[str] = None


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------



@app.get("/health")
def health_check():
    """Simple check to confirm the server is alive."""
    return {"status": "ok"}

@app.post("/webhook/ci")
def receive_ci_event(event: CIBuildEvent):
    """
    Receives a CI/CD build event.

    In the real OmniSight pipeline, a "success" status here is what
    will eventually trigger the Playwright script to run against the
    new staging deployment. For Week 1, we just log and store it.
    """
    record = {
        "received_at": datetime.utcnow().isoformat(),
        "branch": event.branch,
        "commit": event.commit,
        "status": event.status,
        "repository": event.repository,
        "staging_url": event.staging_url,
    }
    received_events.append(record)
    print(f"[webhook] Received build event: {record}")

    # This is the hook point for Week 3/4: if status == "success",
    # kick off the Playwright automation script here.
    if event.status == "success":
        print(f"[webhook] Build succeeded on '{event.branch}' — would trigger OmniSight scan here.")

    return {"received": True, "event": record}


@app.get("/webhook/events")
def list_events():
    """Lists all events received so far - handy for debugging/testing."""
    return {"count": len(received_events), "events": received_events}