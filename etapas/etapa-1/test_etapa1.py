import json

import httpx
import pytest

from app import chat

CORPO = {"messages": [{"role": "user", "content": "O que é uma chave primária?"}]}


def cliente_falso(tratar):
    def criar():
        return httpx.AsyncClient(base_url="http://teste", transport=httpx.MockTransport(tratar))

    return criar


def test_system_prompt_define_o_papel():
    assert len(chat.SYSTEM_PROMPT.strip()) > 30


def test_chat_entrega_os_pedacos_em_ordem(client, monkeypatch):
    linhas = [
        {"message": {"role": "assistant", "content": "Uma chave "}, "done": False},
        {"message": {"role": "assistant", "content": "primária identifica a linha."}, "done": False},
        {"message": {"role": "assistant", "content": ""}, "done": True},
    ]

    def tratar(req: httpx.Request) -> httpx.Response:
        enviado = json.loads(req.content)
        assert enviado["stream"] is True
        assert enviado["messages"][0]["role"] == "system"
        assert enviado["messages"][-1]["content"] == "O que é uma chave primária?"
        return httpx.Response(200, content="\n".join(json.dumps(x) for x in linhas).encode())

    monkeypatch.setattr(chat, "cloud_client", cliente_falso(tratar))
    resp = client.post("/chat", json=CORPO)
    assert resp.status_code == 200
    assert resp.text == "Uma chave primária identifica a linha."


def test_limite_da_conta_vira_erro_429(client, monkeypatch):
    monkeypatch.setattr(chat, "cloud_client", cliente_falso(lambda req: httpx.Response(429)))
    resp = client.post("/chat", json=CORPO)
    assert resp.status_code == 429
    assert "Limite" in resp.json()["erro"]


def test_chave_invalida_vira_erro_401(client, monkeypatch):
    monkeypatch.setattr(chat, "cloud_client", cliente_falso(lambda req: httpx.Response(401)))
    resp = client.post("/chat", json=CORPO)
    assert resp.status_code == 401
    assert "OLLAMA_API_KEY" in resp.json()["erro"]


@pytest.mark.cloud
def test_chat_com_o_modelo_real(client):
    resp = client.post("/chat", json=CORPO)
    assert resp.status_code == 200
    assert resp.text.strip()
