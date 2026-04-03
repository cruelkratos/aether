import uuid
from fastapi import APIRouter, HTTPException
from starlette.status import HTTP_201_CREATED
from app.api.models import SessionCreateResponse, SessionQueryRequest, SessionResponse
from app.agent.agent_loop import AgentLoop

router = APIRouter()
agent_loop = AgentLoop()

sessions = {}


@router.post("/create", response_model=SessionCreateResponse, status_code=HTTP_201_CREATED)
async def create_session():
    session_id = str(uuid.uuid4())
    sessions[session_id] = []
    return SessionCreateResponse(session_id=session_id)


@router.post("/{session_id}/query", response_model=SessionResponse)
async def query_session(session_id: str, request: SessionQueryRequest):
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")

    # store short term messages
    sessions[session_id].append({"role": "user", "content": request.user_prompt})

    result, tool_history = await agent_loop.run(session_id, request.user_prompt, sessions[session_id])

    sessions[session_id].append({"role": "assistant", "content": result})

    return SessionResponse(session_id=session_id, result=result, tool_calls=tool_history)


@router.get("/{session_id}/history")
async def session_history(session_id: str):
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    return {"session_id": session_id, "history": sessions[session_id]}


@router.post("/{session_id}/reset")
async def reset_session(session_id: str):
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    sessions[session_id] = []
    return {"session_id": session_id, "status": "reset"}
