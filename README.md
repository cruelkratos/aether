# Aether: Cloud-Native AI Agent with Tool Use and Memory

## Overview
Local PoC for an AI agent that uses tools and memory layers.

## Prerequisites (Install on your machine)
- Docker Desktop (Windows) or Docker Engine
- Docker Compose
- Git
- Python 3.12+
- pip
- Ollama (via Docker or local install)

## Local setup
1. Clone repository
2. `cd aether`
3. `docker-compose up -d --build`
4. `python -m pip install -r requirements.txt` (for direct host runs)
5. `python scripts/init_db.py`
6. `python scripts/seed_db.py`

## Run API (host)
`uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload`

## Endpoints
- GET `/health/liveness`
- GET `/health/readiness`
- POST `/sessions/create`
- POST `/sessions/{id}/query`
- GET `/sessions/{id}/history`
- POST `/sessions/{id}/reset`

## Testing
`pytest -v`
