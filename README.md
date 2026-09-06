# OmniSight - Self Healing UI

## Project Overview

OmniSight is a self-healing UI automation project designed to detect UI issues, analyze them using AI, and support automated fixes.

## Backend API

The backend is built using FastAPI.

### Health Check

**Endpoint:** `GET /health`

Returns the current health status of the OmniSight API.

### UI Analysis

**Endpoint:** `POST /api/analyze`

Accepts screenshot and DOM data for UI analysis.

#### Request

```json
{
  "screenshot": "test-screenshot",
  "dom": "<button>Login</button>"
}


<!-- OmniSight automated fix test -->


<!-- OmniSight automated fix test -->
