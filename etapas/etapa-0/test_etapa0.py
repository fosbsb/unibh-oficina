import asyncio

import httpx
import pytest

from app import llm
from app.errors import OllamaError


def test_health_responde(client):
    resp = client.get("/health")
    assert resp.status_code == 200
    corpo = resp.json()
    assert corpo["app"] is True
    for chave in ("ollama_local", "modelos_locais", "pgvector", "chave_configurada", "chat_model"):
        assert chave in corpo


def test_chave_invalida_vira_mensagem_clara(monkeypatch):
    def cliente_com_401():
        transporte = httpx.MockTransport(lambda req: httpx.Response(401, json={"error": "unauthorized"}))
        return httpx.AsyncClient(base_url="http://teste", transport=transporte)

    monkeypatch.setattr(llm, "cloud_client", cliente_com_401)
    with pytest.raises(OllamaError) as erro:
        asyncio.run(llm.chat_once([{"role": "user", "content": "oi"}]))
    assert erro.value.status == 401
    assert "OLLAMA_API_KEY" in erro.value.mensagem


def test_chat_once_le_a_resposta(monkeypatch):
    def tratar(req: httpx.Request) -> httpx.Response:
        assert req.url.path == "/api/chat"
        return httpx.Response(200, json={"message": {"role": "assistant", "content": "olá!"}, "done": True})

    def cliente_falso():
        return httpx.AsyncClient(base_url="http://teste", transport=httpx.MockTransport(tratar))

    monkeypatch.setattr(llm, "cloud_client", cliente_falso)
    texto = asyncio.run(llm.chat_once([{"role": "user", "content": "oi"}]))
    assert texto == "olá!"


@pytest.mark.cloud
def test_hello_com_o_modelo_real():
    texto = asyncio.run(llm.chat_once([{"role": "user", "content": "Responda apenas: ok"}]))
    assert isinstance(texto, str) and texto.strip()
