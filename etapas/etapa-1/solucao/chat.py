import json
from collections.abc import AsyncIterator

from app.config import settings
from app.ollama_client import check, cloud_client, cloud_lock

SYSTEM_PROMPT = (
    "Você é um tutor de Banco de Dados para estudantes de graduação. "
    "Explique em português, com exemplos curtos em SQL. "
    "Não entregue a resposta pronta de exercícios: guie o aluno com perguntas. "
    "Se a pergunta fugir de Banco de Dados, diga isso com educação e volte ao tema. "
    "Responda em texto corrido, sem formatação Markdown, com no máximo 150 palavras."
)


async def stream_chat(messages: list[dict]) -> AsyncIterator[str]:
    payload = {
        "model": settings.chat_model,
        "stream": True,
        "messages": [{"role": "system", "content": SYSTEM_PROMPT}, *messages],
    }
    async with (
        cloud_lock,
        cloud_client() as client,
        client.stream("POST", "/api/chat", json=payload) as resp,
    ):
        check(resp)
        async for linha in resp.aiter_lines():
            if not linha:
                continue
            chunk = json.loads(linha)
            pedaco = chunk.get("message", {}).get("content")
            if pedaco:
                yield pedaco
            if chunk.get("done"):
                break
