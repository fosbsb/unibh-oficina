import json

import pytest

from app import quiz
from app.schemas import Quiz


def test_rota_extra_existe(client):
    resp = client.get("/extra/ping")
    assert resp.status_code == 200
    assert resp.json() == {"ok": True}


@pytest.mark.local
def test_quiz_do_material_usa_os_trechos_recuperados(client, monkeypatch):
    recebido = {}

    async def modelo_falso(mensagens, model=None):
        recebido["mensagens"] = mensagens
        questao = {
            "enunciado": "Pergunta?",
            "opcoes": ["a", "b", "c", "d"],
            "correta": 0,
            "explicacao": "Porque sim.",
        }
        return json.dumps({"questoes": [questao]})

    monkeypatch.setattr(quiz, "chat_once", modelo_falso)
    resp = client.post("/extra/quiz-material", json={"tema": "índices", "n": 1})
    assert resp.status_code == 200
    assert len(Quiz.model_validate(resp.json()).questoes) == 1
    assert "03-indices.md" in recebido["mensagens"][-1]["content"]


@pytest.mark.cloud
@pytest.mark.local
def test_quiz_do_material_com_o_modelo_real(client):
    resp = client.post("/extra/quiz-material", json={"tema": "Transações", "n": 2})
    assert resp.status_code == 200
    assert len(Quiz.model_validate(resp.json()).questoes) == 2
