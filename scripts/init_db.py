import asyncio
from app.database import engine
from sqlalchemy import text

async def init():
    async with engine.begin() as conn:
        await conn.execute(text("CREATE TABLE IF NOT EXISTS sessions (id TEXT PRIMARY KEY, data JSONB, created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW())"))
        await conn.execute(text("CREATE TABLE IF NOT EXISTS events (id SERIAL PRIMARY KEY, session_id TEXT, event_type TEXT, payload JSONB, created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW())"))
    print("Database initialized")

if __name__ == "__main__":
    asyncio.run(init())
