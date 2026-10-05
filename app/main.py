import logging
from pathlib import Path

import httpx
import psycopg
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles

from app import extra
from app.chat import stream_chat
from app.config import settings
from app.db import conectar
from app.errors import OllamaError
from app.ollama_client import local_client
from app.quiz import gerar_quiz
from app.rag import ingerir, responder
from app.schemas import AskRequest, ChatRequest, QuizRequest

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(name)s %(message)s")

app = FastAPI(title="Estuda.AI")
app.include_router(extra.router)


@app.exception_handler(OllamaError)
async def tratar_ollama(_: Request, exc: OllamaError):
    return JSONResponse({"erro": exc.mensagem}, status_code=exc.status)


@app.exception_handler(NotImplementedError)
async def tratar_pendente(_: Request, exc: NotImplementedError):
    return JSONResponse({"erro": f"Ainda não implementado. {exc}"}, status_code=501)


@app.exception_handler(httpx.HTTPError)
async def tratar_rede(_: Request, exc: httpx.HTTPError):
    return JSONResponse(
        {"erro": "Não consegui falar com um dos serviços. Veja 'docker compose ps' e a conexão."},
        status_code=503,
    )


@app.exception_handler(Exception)
async def tratar_geral(_: Request, exc: Exception):
    logging.getLogger("app").exception("erro inesperado")
    return JSONResponse({"erro": f"Erro inesperado: {exc}"}, status_code=500)


@app.get("/health")
async def health():
    ollama_local = False
    modelos_locais = False
    try:
        async with local_client() as client:
            resp = await client.get("/api/tags")
        ollama_local = resp.status_code == 200
        nomes = [m["name"] for m in resp.json().get("models", [])]
        modelos_locais = any(n.startswith(settings.embed_model) for n in nomes)
    except httpx.HTTPError:
        pass

    pgvector = False
    try:
        with conectar() as conn:
            conn.execute("SELECT 1")
        pgvector = True
    except psycopg.Error as erro:
        logging.getLogger("app").warning("pgvector indisponível: %s", erro)

    return {
        "app": True,
        "ollama_local": ollama_local,
        "modelos_locais": modelos_locais,
        "pgvector": pgvector,
        "chave_configurada": bool(settings.ollama_api_key)
        and settings.ollama_api_key != "cole-sua-chave-aqui",
        "chat_model": settings.chat_model,
    }


@app.post("/chat")
async def chat(req: ChatRequest):
    geracao = stream_chat([m.model_dump() for m in req.messages])
    try:
        primeiro = await anext(geracao)
    except StopAsyncIteration:
        primeiro = ""

    async def corpo():
        yield primeiro
        try:
            async for pedaco in geracao:
                yield pedaco
        except (OllamaError, httpx.HTTPError) as exc:
            yield f"\n[erro] {exc}"

    return StreamingResponse(corpo(), media_type="text/plain; charset=utf-8")


@app.post("/quiz")
async def quiz(req: QuizRequest):
    return await gerar_quiz(req.tema, req.n)


@app.post("/ingest")
async def ingest():
    return {"trechos_indexados": await ingerir()}


@app.post("/ask")
async def ask(req: AskRequest):
    return await responder(req.pergunta, req.k)


app.mount("/", StaticFiles(directory=Path(__file__).parent / "static", html=True), name="static")
