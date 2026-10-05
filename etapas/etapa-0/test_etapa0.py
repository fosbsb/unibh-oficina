import asyncio
import time

import httpx
import pytest

from app import llm
from app.config import settings
from app.errors import OllamaError


def test_health_responde(client):
    """O app está de pé e o /health mostra o estado de cada serviço."""
    resp = client.get("/health")
    corpo = resp.json()
    print(f"\nGET /health -> {resp.status_code}")
    for chave, valor in corpo.items():
        print(f"  {chave}: {valor}")
    assert resp.status_code == 200
    assert corpo["app"] is True
    for chave in ("ollama_local", "modelos_locais", "pgvector", "chave_configurada", "chat_model"):
        assert chave in corpo


def test_chave_invalida_vira_mensagem_clara(monkeypatch):
    """Uma resposta 401 da nuvem vira uma mensagem que o aluno entende."""

    def cliente_com_401():
        transporte = httpx.MockTransport(lambda req: httpx.Response(401, json={"error": "unauthorized"}))
        return httpx.AsyncClient(base_url="http://teste", transport=transporte)

    monkeypatch.setattr(llm, "cloud_client", cliente_com_401)
    with pytest.raises(OllamaError) as erro:
        asyncio.run(llm.chat_once([{"role": "user", "content": "oi"}]))
    print("\nnuvem simulada respondeu 401")
    print(f"  status do erro: {erro.value.status}")
    print(f"  mensagem: {erro.value.mensagem}")
    assert erro.value.status == 401
    assert "OLLAMA_API_KEY" in erro.value.mensagem


def test_chat_once_le_a_resposta(monkeypatch):
    """chat_once envia a requisição certa e devolve o texto da resposta."""
    enviado = {}

    def tratar(req: httpx.Request) -> httpx.Response:
        enviado["caminho"] = req.url.path
        enviado["corpo"] = req.content.decode()
        return httpx.Response(200, json={"message": {"role": "assistant", "content": "olá!"}, "done": True})

    def cliente_falso():
        return httpx.AsyncClient(base_url="http://teste", transport=httpx.MockTransport(tratar))

    monkeypatch.setattr(llm, "cloud_client", cliente_falso)
    texto = asyncio.run(llm.chat_once([{"role": "user", "content": "oi"}]))
    print("\nnuvem simulada")
    print(f"  o app chamou: POST {enviado['caminho']}")
    print(f"  corpo enviado: {enviado['corpo']}")
    print(f"  texto devolvido por chat_once: {texto!r}")
    assert enviado["caminho"] == "/api/chat"
    assert texto == "olá!"


def test_endpoint_hello_devolve_a_resposta_do_modelo(client, monkeypatch):
    """O cartão "Conexão" da tela usa o POST /hello, que chama o seu chat_once."""

    def cliente_falso():
        resposta = {"message": {"role": "assistant", "content": "olá, aluno!"}, "done": True}
        return httpx.AsyncClient(
            base_url="http://teste", transport=httpx.MockTransport(lambda req: httpx.Response(200, json=resposta))
        )

    monkeypatch.setattr(llm, "cloud_client", cliente_falso)
    resp = client.post("/hello", json={"mensagem": "oi"})
    print(f"\nPOST /hello -> {resp.status_code} {resp.json()}")
    assert resp.status_code == 200
    assert resp.json() == {"modelo": settings.chat_model, "resposta": "olá, aluno!"}


@pytest.mark.cloud
def test_hello_com_o_modelo_real():
    """Chamada de verdade ao Ollama Cloud com a chave do aluno."""
    pergunta = "Responda apenas: ok"
    inicio = time.perf_counter()
    texto = asyncio.run(llm.chat_once([{"role": "user", "content": pergunta}]))
    duracao = time.perf_counter() - inicio
    print(f"\nOllama Cloud ({settings.ollama_cloud_url}) · modelo {settings.chat_model}")
    print(f"  pergunta: {pergunta!r}")
    print(f"  resposta: {texto.strip()!r}")
    print(f"  tempo: {duracao:.1f}s")
    assert isinstance(texto, str) and texto.strip()
