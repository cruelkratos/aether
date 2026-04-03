import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    redis_url: str = os.getenv("REDIS_URL", "redis://localhost:6379")
    database_url: str = os.getenv("DATABASE_URL", "postgresql+asyncpg://aether:aether_pass@localhost:5432/aether_db")
    qdrant_url: str = os.getenv("QDRANT_URL", "http://localhost:6333")
    ollama_url: str = os.getenv("OLLAMA_URL", "http://localhost:11434")
    agent_max_iterations: int = 5
    short_term_history: int = 20
    disable_tool_sandbox: bool = os.getenv("DISABLE_TOOL_SANDBOX", "false").lower() in ("1", "true")

    class Config:
        env_file = ".env"


settings = Settings()
