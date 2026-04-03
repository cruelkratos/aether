import asyncpg
from app.config import settings

async def sql_query(query: str) -> dict:
    # keep it safe: only SELECT statements
    q = query.strip().lower()
    if not q.startswith("select"):
        return {"error": "Only SELECT queries allowed"}
    conn = await asyncpg.connect(settings.database_url.replace("postgresql+asyncpg://", "postgresql://"))
    try:
        rows = await conn.fetch(query)
        return {"rows": [dict(r) for r in rows]}
    finally:
        await conn.close()
