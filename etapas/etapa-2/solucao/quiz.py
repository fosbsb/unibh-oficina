from pydantic import ValidationError

from app.config import settings
from app.errors import OllamaError
from app.llm import chat_once
from app.schemas import Quiz

SISTEMA = (
    "Você gera quizzes de Banco de Dados em português. "
    "Responda SOMENTE com JSON, sem texto antes ou depois, neste formato: "
    '{"questoes":[{"enunciado":"...","opcoes":["A","B","C","D"],"correta":0,"explicacao":"..."}]}. '
    'Cada questão tem exatamente 4 opções e "correta" é o índice (0 a 3) da opção certa.'
)


def extrair_json(texto: str) -> str:
    inicio, fim = texto.find("{"), texto.rfind("}")
    if inicio == -1 or fim == -1 or fim < inicio:
        raise ValueError("nenhum objeto JSON encontrado na resposta")
    return texto[inicio : fim + 1]


async def gerar_quiz(tema: str, n: int, contexto: str = "") -> Quiz:
    pedido = f"Gere {n} questões sobre: {tema}."
    if contexto:
        pedido += f"\n\nUse como base apenas este material:\n{contexto}"
    mensagens = [
        {"role": "system", "content": SISTEMA},
        {"role": "user", "content": pedido},
    ]
    ultimo_erro: Exception | None = None
    for _ in range(1 + settings.quiz_max_retries):
        texto = await chat_once(mensagens)
        try:
            return Quiz.model_validate_json(extrair_json(texto))
        except (ValidationError, ValueError) as erro:
            ultimo_erro = erro
            mensagens += [
                {"role": "assistant", "content": texto},
                {"role": "user", "content": f"O JSON é inválido ({erro}). Responda só com o JSON corrigido."},
            ]
    raise OllamaError(f"O modelo não devolveu um quiz válido: {ultimo_erro}", 502)
