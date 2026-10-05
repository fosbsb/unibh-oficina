from pydantic import ValidationError

from app.config import settings
from app.errors import OllamaError
from app.llm import chat_once
from app.schemas import Quiz

SISTEMA = ""


def extrair_json(texto: str) -> str:
    # ETAPA 2 - o modelo pode devolver texto extra ou cercas ```json.
    # Devolva só o trecho entre o primeiro "{" e o último "}"; se não houver, levante ValueError.
    raise NotImplementedError("Etapa 2: implemente extrair_json em app/quiz.py")


async def gerar_quiz(tema: str, n: int, contexto: str = "") -> Quiz:
    # ETAPA 2 - peça um quiz em JSON, valide e tente de novo se vier inválido.
    #   1. Preencha SISTEMA: peça SOMENTE JSON no formato de Quiz, com um exemplo.
    #   2. Monte as mensagens [system, user]; se houver contexto, inclua-o na mensagem do usuário.
    #   3. Repita 1 + settings.quiz_max_retries vezes:
    #        texto = await chat_once(msgs)
    #        tente Quiz.model_validate_json(extrair_json(texto))
    #        se falhar (ValidationError ou ValueError), acrescente a resposta do modelo e o erro
    #        às mensagens e peça o JSON corrigido.
    #   4. Se todas as tentativas falharem, levante OllamaError(mensagem, 502).
    raise NotImplementedError("Etapa 2: implemente gerar_quiz em app/quiz.py")
