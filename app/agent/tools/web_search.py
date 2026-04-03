import httpx

async def web_search(query: str) -> dict:
    url = "https://api.duckduckgo.com/"
    params = {"q": query, "format": "json", "no_redirect": 1}
    async with httpx.AsyncClient(timeout=20.0) as client:
        r = await client.get(url, params=params)
        r.raise_for_status()
        data = r.json()
        summary = data.get("AbstractText") or data.get("RelatedTopics", [])
        return {"query": query, "summary": summary, "raw": data}
