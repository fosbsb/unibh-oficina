import asyncio
import json

import pytest
from pydantic import ValidationError

from app import quiz
from app.errors import OllamaError
from app.schemas import Questao, Quiz


def questao(**mudancas):
    base = {
        "enunciado": "Pergunta?",
        "opcoes": ["a", "b", "c", "d"],
        "correta": 1,
        "explicacao": "Porque sim.",
    }
    return {**base, **mudancas}


def quiz_json(n=1):
    return json.dumps({"questoes": [questao() for _ in range(n)]})


def modelo_falso(monkeypatch, respostas):
    chamadas = []

    async def falso(mensagens, model=None):
        chamadas.append(list(mensagens))
        return respostas[min(len(chamadas), len(respostas)) - 1]

    monkeypatch.setattr(quiz, "chat_once", falso)
    return chamadas


def test_schema_aceita_o_exemplo(quiz_exemplo):
    assert len(Quiz.model_validate(quiz_exemplo).questoes) == 1


@pytest.mark.parametrize(
    "mudanca",
    [{"opcoes": ["a", "b", "c"]}, {"correta": 4}, {"correta": -1}, {"enunciado": ""}],
)
def test_schema_recusa_questao_invalida(mudanca):
    with pytest.raises(ValidationError):
        Questao.model_validate(questao(**mudanca))


def test_schema_recusa_quiz_vazio():
    with pytest.raises(ValidationError):
        Quiz.model_validate({"questoes": []})


def test_extrair_json_ignora_cercas_e_texto_extra():
    texto = 'Claro! ```json\n{"a": 1}\n``` Espero que ajude.'
    assert json.loads(quiz.extrair_json(texto)) == {"a": 1}


def test_extrair_json_sem_objeto_levanta_erro():
    with pytest.raises(ValueError):
        quiz.extrair_json("sem json aqui")


def test_gerar_quiz_valido_de_primeira(monkeypatch):
    chamadas = modelo_falso(monkeypatch, [quiz_json(3)])
    resultado = asyncio.run(quiz.gerar_quiz("índices", 3))
    assert len(resultado.questoes) == 3
    assert len(chamadas) == 1


def test_gerar_quiz_tenta_de_novo_quando_o_json_e_invalido(monkeypatch):
    chamadas = modelo_falso(monkeypatch, ["isto não é json", quiz_json()])
    resultado = asyncio.run(quiz.gerar_quiz("índices", 1))
    assert len(resultado.questoes) == 1
    assert len(chamadas) == 2
    assert any("inválido" in m["content"] for m in chamadas[1] if m["role"] == "user")


def test_gerar_quiz_desiste_depois_dos_retries(monkeypatch):
    chamadas = modelo_falso(monkeypatch, ["lixo"])
    with pytest.raises(OllamaError) as erro:
        asyncio.run(quiz.gerar_quiz("índices", 1))
    assert erro.value.status == 502
    assert len(chamadas) == 3


def test_endpoint_quiz_devolve_json_valido(client, monkeypatch):
    modelo_falso(monkeypatch, [quiz_json(2)])
    resp = client.post("/quiz", json={"tema": "índices", "n": 2})
    assert resp.status_code == 200
    assert len(resp.json()["questoes"]) == 2


def test_endpoint_quiz_com_json_quebrado_devolve_502(client, monkeypatch):
    modelo_falso(monkeypatch, ["lixo"])
    resp = client.post("/quiz", json={"tema": "índices", "n": 2})
    assert resp.status_code == 502
    assert "quiz válido" in resp.json()["erro"]


@pytest.mark.cloud
def test_quiz_com_o_modelo_real(client):
    resp = client.post("/quiz", json={"tema": "Índices", "n": 3})
    assert resp.status_code == 200
    assert len(Quiz.model_validate(resp.json()).questoes) == 3
