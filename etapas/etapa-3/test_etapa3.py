import asyncio

import pytest

from app import rag
from app.config import settings

pytestmark = pytest.mark.local


@pytest.fixture(scope="module")
def indexado():
    return asyncio.run(rag.ingerir())


def test_ingestao_indexa_todos_os_trechos(indexado):
    assert indexado == len(rag.carregar_chunks())
    assert indexado >= 15


def test_recuperacao_acha_a_fonte_esperada(indexado, perguntas):
    acertos = []
    for item in perguntas:
        [vetor] = asyncio.run(rag.embed([rag.texto_de_pergunta(item["pergunta"])]))
        fontes = [c["fonte"] for c in rag.buscar(vetor, settings.rag_top_k)]
        acertos.append(item["fonte_esperada"] in fontes)
    assert sum(acertos) >= 8, f"só {sum(acertos)} de {len(acertos)} perguntas acharam a fonte"


def test_pergunta_fora_do_corpus_nao_chama_o_modelo(indexado, monkeypatch):
    async def nao_deve_chamar(*args, **kwargs):
        raise AssertionError("o modelo da nuvem não deveria ser chamado")

    monkeypatch.setattr(rag, "chat_once", nao_deve_chamar)
    resultado = asyncio.run(rag.responder("Qual é a capital da França?"))
    assert resultado["fontes"] == []
    assert "Não encontrei" in resultado["resposta"]


def test_reranker_indisponivel_nao_derruba_o_rag(indexado, monkeypatch):
    async def resposta_falsa(mensagens, model=None):
        return "Resposta de teste [1]."

    monkeypatch.setattr(rag, "chat_once", resposta_falsa)
    monkeypatch.setattr(settings, "rerank_model", "modelo-que-nao-existe")
    resultado = asyncio.run(rag.responder("Quando um índice pode deixar o banco mais lento?"))
    assert resultado["fontes"]
    assert resultado["resposta"] == "Resposta de teste [1]."


def test_pontuar_converte_logprobs_em_probabilidade():
    resposta = {
        "logprobs": [
            {
                "top_logprobs": [
                    {"token": "yes", "logprob": -0.2231435513},
                    {"token": "no", "logprob": -1.6094379124},
                    {"token": "ok", "logprob": -3.0},
                ]
            }
        ]
    }
    assert rag.pontuar(resposta) == pytest.approx(0.8, abs=1e-3)


def test_pontuar_recusa_resposta_sem_yes_ou_no():
    resposta = {"logprobs": [{"top_logprobs": [{"token": "3", "logprob": -11.9}]}]}
    with pytest.raises(ValueError):
        rag.pontuar(resposta)


def test_reranker_poe_o_trecho_certo_na_frente(indexado):
    pergunta = "Quando um índice pode deixar o banco mais lento?"
    [vetor] = asyncio.run(rag.embed([rag.texto_de_pergunta(pergunta)]))
    ordenados = asyncio.run(rag.rerank(pergunta, rag.buscar(vetor, settings.rag_top_k)))
    assert all(0.0 <= c["rerank"] <= 1.0 for c in ordenados)
    assert ordenados[0]["fonte"] == "03-indices.md"
    assert ordenados[0]["rerank"] > 0.5
    assert [c["rerank"] for c in ordenados] == sorted((c["rerank"] for c in ordenados), reverse=True)


def test_resposta_usa_os_trechos_recuperados(indexado, monkeypatch):
    recebido = {}

    async def modelo_falso(mensagens, model=None):
        recebido["mensagens"] = mensagens
        return "Resposta [1]."

    monkeypatch.setattr(rag, "chat_once", modelo_falso)
    resultado = asyncio.run(rag.responder("Qual a diferença entre WHERE e HAVING?"))
    contexto = recebido["mensagens"][-1]["content"]
    assert "[1]" in contexto
    assert any(f["fonte"] == "05-consultas-sql.md" for f in resultado["fontes"])


def test_endpoint_ask_devolve_resposta_e_fontes(indexado, client, monkeypatch):
    async def modelo_falso(mensagens, model=None):
        return "Atomicidade é tudo ou nada [1]."

    monkeypatch.setattr(rag, "chat_once", modelo_falso)
    resp = client.post("/ask", json={"pergunta": "O que é atomicidade em uma transação?"})
    assert resp.status_code == 200
    assert resp.json()["fontes"][0]["fonte"] == "04-transacoes.md"


@pytest.mark.cloud
def test_resposta_real_cita_a_fonte(indexado, client):
    resp = client.post("/ask", json={"pergunta": "Quando um índice pode deixar o banco mais lento?"})
    assert resp.status_code == 200
    assert resp.json()["fontes"][0]["fonte"] == "03-indices.md"
    assert "[1]" in resp.json()["resposta"]
