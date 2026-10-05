import json
import logging
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app.config import settings
from app.main import app

RAIZ = Path(__file__).parent

logging.getLogger("httpx").setLevel(logging.WARNING)


def pytest_collection_modifyitems(config, items):
    sem_chave = pytest.mark.skip(reason="OLLAMA_API_KEY não configurada no .env")
    for item in items:
        if "cloud" in item.keywords and settings.ollama_api_key in ("", "cole-sua-chave-aqui"):
            item.add_marker(sem_chave)


@pytest.fixture
def client():
    return TestClient(app, raise_server_exceptions=False)


@pytest.fixture
def perguntas():
    return json.loads((RAIZ / "etapas" / "perguntas.json").read_text(encoding="utf-8"))


@pytest.fixture
def quiz_exemplo():
    return json.loads((RAIZ / "etapas" / "quiz_exemplo.json").read_text(encoding="utf-8"))
