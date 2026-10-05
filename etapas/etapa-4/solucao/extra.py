from fastapi import APIRouter
from pydantic import BaseModel, Field

from app.config import settings
from app.quiz import gerar_quiz
from app.rag import buscar, embed, rerank, texto_de_pergunta
from app.schemas import Quiz

router = APIRouter(prefix="/extra", tags=["extra"])


class QuizMaterialRequest(BaseModel):
    tema: str = Field(min_length=2)
    n: int = Field(default=3, ge=1, le=10)


@router.get("/ping")
async def ping() -> dict:
    return {"ok": True}


@router.post("/quiz-material", response_model=Quiz)
async def quiz_material(req: QuizMaterialRequest) -> Quiz:
    [vetor] = await embed([texto_de_pergunta(req.tema)])
    trechos = await rerank(req.tema, buscar(vetor, settings.rag_top_k))
    contexto = "\n\n".join(f"({t['fonte']}) {t['trecho']}" for t in trechos)
    return await gerar_quiz(req.tema, req.n, contexto)
