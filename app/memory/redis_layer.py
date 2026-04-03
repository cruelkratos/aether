import redis.asyncio as aioredis
from app.config import settings

class RedisMemory:
    def __init__(self):
        self.redis = aioredis.from_url(settings.redis_url, encoding="utf-8", decode_responses=True)

    async def get_session(self, session_id: str):
        data = await self.redis.lrange(f"session:{session_id}", 0, -1)
        return "\n".join(data) if data else ""

    async def append_message(self, session_id: str, message: dict):
        serialized = str(message)
        await self.redis.rpush(f"session:{session_id}", serialized)
        await self.redis.expire(f"session:{session_id}", 86400)  # 24h
