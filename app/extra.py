from fastapi import APIRouter

router = APIRouter(prefix="/extra", tags=["extra"])


@router.get("/ping")
async def ping() -> dict:
    # ETAPA 4 - desafio livre. Sugestão: crie POST /extra/quiz-material, que gera um quiz
    # usando como contexto os trechos recuperados pelo RAG (reaproveite embed, buscar e gerar_quiz).
    return {"ok": True}
