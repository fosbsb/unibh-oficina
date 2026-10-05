import json
from collections.abc import AsyncIterator

from app.config import settings
from app.ollama_client import check, cloud_client, cloud_lock

SYSTEM_PROMPT = ""


async def stream_chat(messages: list[dict]) -> AsyncIterator[str]:
    # ETAPA 1 - escreva o SYSTEM_PROMPT acima (o papel de tutor de Banco de Dados) e
    # implemente o streaming:
    #   1. Monte o payload com "stream": True e a lista [system, *messages].
    #   2. Use "async with cloud_lock, cloud_client() as client:" e
    #      "async with client.stream('POST', '/api/chat', json=payload) as resp:".
    #   3. Chame check(resp) e percorra "async for linha in resp.aiter_lines()".
    #   4. Cada linha é um JSON; entregue chunk["message"]["content"] com yield
    #      e pare quando chunk["done"] for verdadeiro.
    raise NotImplementedError("Etapa 1: implemente stream_chat em app/chat.py")
    yield ""
