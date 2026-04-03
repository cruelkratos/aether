import httpx
from app.config import settings


class OllamaLLM:
    async def generate(self, prompt: str) -> str:
        url = f"{settings.ollama_url}/api/completions"
        payload = {
            "model": "llama2",
            "prompt": prompt,
            "max_tokens": 400,
            "temperature": 0.2,
        }
        async with httpx.AsyncClient() as client:
            r = await client.post(url, json=payload, timeout=60.0)
            r.raise_for_status()
            data = r.json()
            if "choices" in data and len(data["choices"]) > 0:
                return data["choices"][0].get("text", "")
            return ""
