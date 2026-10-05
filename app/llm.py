from app.config import settings
from app.ollama_client import check, cloud_client, cloud_lock


async def chat_once(messages: list[dict], model: str | None = None) -> str:
    # ETAPA 0 - envie as mensagens ao modelo e devolva o texto da resposta.
    #   1. Monte o payload: {"model": ..., "messages": ..., "stream": False}
    #      (use settings.chat_model quando model for None).
    #   2. Dentro de "async with cloud_lock, cloud_client() as client:", faça
    #      client.post("/api/chat", json=payload).
    #   3. Chame check(resp) para traduzir erros (chave inválida, limite, etc.).
    #   4. Devolva resp.json()["message"]["content"].
    raise NotImplementedError("Etapa 0: implemente chat_once em app/llm.py")
