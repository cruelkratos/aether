from app.database import async_session

class PostgresMemory:
    async def upsert_tool_call(self, session_id: str, tool_call: dict, output: any):
        # TODO: implement SQL persistence using SQLAlchemy models
        pass

    async def upsert_response(self, session_id: str, response: str):
        # TODO: implement SQL persistence using SQLAlchemy models
        pass
