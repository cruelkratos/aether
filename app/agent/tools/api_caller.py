import httpx

async def call_api(method: str = "GET", url: str = "", headers: dict = None, params: dict = None, body: dict = None):
    method = method.upper()
    if method not in ["GET", "POST", "PUT", "DELETE", "PATCH"]:
        return {"error": "Unsupported method"}

    async with httpx.AsyncClient(timeout=30.0) as client:
        r = await client.request(method, url, headers=headers or {}, params=params or {}, json=body)
        return {"status_code": r.status_code, "body": r.text}
