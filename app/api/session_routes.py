import uuid
import asyncio
from fastapi import APIRouter, HTTPException, BackgroundTasks
from starlette.status import HTTP_201_CREATED
from app.api.models import SessionCreateResponse, SessionQueryRequest, SessionResponse
from app.agent.agent_loop import AgentLoop
from app.agent.llm_interface import OllamaLLM
from app.memory.memory_handler import MemoryHandler

router = APIRouter()
agent_loop = AgentLoop()
memory = MemoryHandler()

# In-memory session store (for short-term demo; use DB in production)
sessions = {}

# LLM warmup: keep the model loaded in Ollama's memory
async def _warmup_llm():
    try:
        llm = OllamaLLM()
        await llm.generate("hi", max_tokens=1)
    except Exception:
        pass


@router.post("/create", response_model=SessionCreateResponse, status_code=HTTP_201_CREATED)
async def create_session(background_tasks: BackgroundTasks):
    """Create a new agent session and pre-warm the LLM."""
    session_id = str(uuid.uuid4())
    sessions[session_id] = []
    background_tasks.add_task(_warmup_llm)
    return SessionCreateResponse(session_id=session_id)


@router.post("/{session_id}/query", response_model=SessionResponse)
async def query_session(session_id: str, request: SessionQueryRequest):
    """Send a query to the agent."""
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")

    # Run agent with session history
    result, tool_history = await agent_loop.run(session_id, request.user_prompt, sessions[session_id])

    # Update session history
    sessions[session_id].append({"role": "user", "content": request.user_prompt})
    sessions[session_id].append({"role": "assistant", "content": result})

    return SessionResponse(
        session_id=session_id,
        result=result,
        tool_calls=tool_history
    )


@router.get("/{session_id}/history")
async def session_history(session_id: str):
    """Get conversation history for a session."""
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    return {"session_id": session_id, "history": sessions[session_id]}


@router.post("/{session_id}/reset")
async def reset_session(session_id: str):
    """Reset a session's history and memory."""
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    sessions[session_id] = []
    await memory.clear_session(session_id)
    return {"session_id": session_id, "status": "reset"}


@router.delete("/{session_id}")
async def delete_session(session_id: str):
    """Delete a session."""
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    await memory.clear_session(session_id)
    del sessions[session_id]
    return {"session_id": session_id, "status": "deleted"}
