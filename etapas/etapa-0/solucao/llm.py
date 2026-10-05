from app.config import settings
from app.ollama_client import check, cloud_client, cloud_lock


async def chat_once(messages: list[dict], model: str | None = None) -> str:
    payload = {
        "model": model or settings.chat_model,
        "messages": messages,
        "stream": False,
    }
    async with cloud_lock, cloud_client() as client:
        resp = await client.post("/api/chat", json=payload)
    check(resp)
    return resp.json()["message"]["content"]
