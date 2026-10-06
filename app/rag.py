import logging
from pathlib import Path

from pgvector import Vector

from app.config import settings
from app.db import conectar
from app.llm import chat_once
from app.ollama_client import local_client

log = logging.getLogger("rag")

CORPUS = Path(__file__).resolve().parent.parent / "corpus"


def carregar_chunks() -> list[dict]:
    chunks = []
    for arquivo in sorted(CORPUS.glob("*.md")):
        texto = arquivo.read_text(encoding="utf-8")
        for bloco in texto.split("\n## ")[1:]:
            titulo, _, corpo = bloco.partition("\n")
            chunks.append(
                {
                    "fonte": arquivo.name,
                    "titulo": titulo.strip(),
                    "trecho": f"{titulo.strip()}\n{corpo.strip()}",
                }
            )
    return chunks


def texto_de_trecho(chunk: dict) -> str:
    # Prefixo de tarefa para os trechos do material (já pronto; use em ingerir).
    return f"title: {chunk['titulo']} | text: {chunk['trecho']}"


def texto_de_pergunta(pergunta: str) -> str:
    # Prefixo de tarefa para perguntas (já pronto; use antes de embed na busca).
    return f"task: search result | query: {pergunta}"


async def embed(textos: list[str]) -> list[list[float]]:
    # ETAPA 3 (1/5) - transforme textos em vetores usando o Ollama LOCAL.
    #   POST /api/embed com {"model": settings.embed_model, "input": textos}
    #   (use "async with local_client() as client"). A resposta tem a chave "embeddings".
    #   Dica: o modelo rende melhor com prefixos de tarefa. Use texto_de_trecho(chunk) para os
    #   trechos e texto_de_pergunta(pergunta) para a pergunta (já estão prontas acima).
    raise NotImplementedError("Etapa 3: implemente embed em app/rag.py")


async def ingerir() -> int:
    # ETAPA 3 (2/5) - indexe o material no pgvector.
    #   1. chunks = carregar_chunks()
    #   2. vetores = await embed([...um texto por chunk...])
    #   3. com "with conectar() as conn:", apague a tabela (TRUNCATE chunks) e faça INSERT
    #      de (fonte, titulo, trecho, embedding) para cada chunk, passando Vector(vetor).
    #   4. devolva quantos trechos foram indexados.
    raise NotImplementedError("Etapa 3: implemente ingerir em app/rag.py")


def buscar(vetor: list[float], k: int) -> list[dict]:
    # ETAPA 3 (3/5) - busque os k trechos mais parecidos com a pergunta.
    #   SELECT fonte, titulo, trecho, 1 - (embedding <=> %s) AS similaridade
    #   FROM chunks ORDER BY embedding <=> %s LIMIT %s
    #   (o operador <=> é a distância de cosseno; passe Vector(vetor) nos parâmetros).
    #   Devolva uma lista de dicts com fonte, titulo, trecho e similaridade (float).
    raise NotImplementedError("Etapa 3: implemente buscar em app/rag.py")


def pontuar(resposta: dict) -> float:
    # ETAPA 3 (4/5, opcional) - converta a resposta do reranker em uma nota de 0 a 1.
    #   Os tokens candidatos estão em resposta["logprobs"][0]["top_logprobs"], cada um com
    #   "token" e "logprob". Some exp(logprob) dos tokens "yes" (P_yes) e "no" (P_no), ignorando
    #   maiúsculas e espaços ("Yes" conta como "yes"), e devolva P_yes / (P_yes + P_no).
    #   Se nenhum token for yes/no, levante ValueError. (import math)
    raise NotImplementedError("Etapa 3: implemente pontuar em app/rag.py")


async def rerank(pergunta: str, candidatos: list[dict]) -> list[dict]:
    # ETAPA 3 (4/5, opcional) - reordene os candidatos com o modelo de reranking local.
    #   Para cada candidato, chame POST /api/generate com raw=True, stream=False,
    #   options {"temperature": 0, "num_predict": 1}, logprobs=True e top_logprobs=20.
    #   O prompt segue o formato do Qwen3-Reranker: system com a regra "yes"/"no",
    #   user com <Instruct>, <Query> e <Document>, e o início da resposta do assistente
    #   com um bloco <think></think> vazio. O score é P(yes) / (P(yes) + P(no)),
    #   calculado por pontuar(resposta), a partir dos tokens "yes" e "no".
    #   Devolva os candidatos com a chave "rerank" (o score), do maior para o menor.
    #   Se qualquer coisa falhar, devolva os candidatos na ordem original.
    # Enquanto não implementar, os candidatos seguem na ordem da busca vetorial.
    return candidatos


async def responder(pergunta: str, k: int | None = None) -> dict:
    # ETAPA 3 (5/5) - monte a resposta ancorada no material.
    #   1. vetor = embed da pergunta; candidatos = buscar(vetor, k or settings.rag_top_k)
    #   2. candidatos = await rerank(pergunta, candidatos)
    #   3. relevantes = candidatos com similaridade >= settings.sim_min
    #   4. se não houver relevantes, devolva {"resposta": "Não encontrei isso no material.",
    #      "fontes": []} sem chamar o modelo
    #   5. senão, monte o contexto numerado [1], [2]... e peça ao modelo (chat_once) que responda
    #      só com base nos trechos, citando as fontes
    #   6. devolva {"resposta": texto, "fontes": relevantes}
    raise NotImplementedError("Etapa 3: implemente responder em app/rag.py")
