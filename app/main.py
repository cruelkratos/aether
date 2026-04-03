from fastapi import FastAPI
from app.api.session_routes import router as session_router

app = FastAPI(title="Aether AI Agent", version="0.1.0")

app.include_router(session_router, prefix="/sessions", tags=["sessions"])


@app.get("/health/liveness")
async def liveness():
    return {"status": "alive"}


@app.get("/health/readiness")
async def readiness():
    return {"status": "ready"}
