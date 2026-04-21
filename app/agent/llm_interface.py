import logging
import httpx
from app.config import settings

logger = logging.getLogger(__name__)


class OllamaLLM:
    def __init__(self):
        self.base_url = settings.ollama_url
        # Use model available in Ollama container; pull llama2 in Docker Compose setup
        self.model = "llama3"

    async def generate(self, prompt: str, max_tokens: int = 512) -> str:
        """Generate text using Ollama LLM."""
        url = f"{self.base_url}/api/generate"
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.2,
                "num_predict": max_tokens,
                "top_p": 0.9,
            }
        }
        
        try:
            logger.info(f"LLM request: model={self.model}, prompt_len={len(prompt)}, max_tokens={max_tokens}")
            async with httpx.AsyncClient(timeout=120.0) as client:
                response = await client.post(url, json=payload)
                response.raise_for_status()
                data = response.json()
                result = data.get("response", "").strip()
                duration = data.get("total_duration", 0) / 1e9  # nanoseconds to seconds
                logger.info(f"LLM response: {len(result)} chars, duration={duration:.1f}s")
                return result
        except Exception as e:
            logger.error(f"LLM error: {e}")
            return f"LLM Error: {str(e)}"
