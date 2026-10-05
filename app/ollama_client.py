import asyncio

import httpx

from app.config import settings
from app.errors import OllamaError

cloud_lock = asyncio.Lock()


def cloud_client() -> httpx.AsyncClient:
    return httpx.AsyncClient(
        base_url=settings.ollama_cloud_url,
        headers={"Authorization": f"Bearer {settings.ollama_api_key}"},
        timeout=httpx.Timeout(120.0, connect=10.0),
    )


def local_client() -> httpx.AsyncClient:
    return httpx.AsyncClient(
        base_url=settings.ollama_local_url,
        timeout=httpx.Timeout(120.0, connect=5.0),
    )


def check(resp: httpx.Response) -> None:
    if resp.status_code == 401:
        raise OllamaError("Chave inválida ou ausente. Confira OLLAMA_API_KEY no arquivo .env.", 401)
    if resp.status_code == 404:
        raise OllamaError(
            f"Modelo '{settings.chat_model}' não encontrado na nuvem. Confira CHAT_MODEL no .env.",
            404,
        )
    if resp.status_code == 429:
        raise OllamaError("Limite da conta atingido. Aguarde alguns segundos e tente de novo.", 429)
    if resp.status_code >= 400:
        raise OllamaError(f"O Ollama Cloud respondeu com erro {resp.status_code}.", 502)
