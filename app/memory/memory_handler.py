from typing import List, Dict, Any
from .redis_layer import RedisMemory
from .postgres_layer import PostgresMemory
from .qdrant_layer import QdrantMemory

class MemoryHandler:
    def __init__(self):
        self.redis = RedisMemory()
        self.postgres = PostgresMemory()
        self.qdrant = QdrantMemory()

    async def retrieve(self, session_id: str, history: List[Dict[str, Any]]):
        short = await self.redis.get_session(session_id)
        sem = await self.qdrant.search(session_id, history)
        return "\n".join([short or "", sem or ""])

    async def save_tool_result(self, session_id: str, tool_call: Dict[str, Any], output: Any):
        await self.redis.append_message(session_id, {"tool": tool_call, "result": output})
        await self.postgres.upsert_tool_call(session_id, tool_call, output)

    async def save_final_response(self, session_id: str, response: str):
        await self.redis.append_message(session_id, {"assistant": response})
        await self.postgres.upsert_response(session_id, response)
