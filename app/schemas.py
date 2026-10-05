from pydantic import BaseModel, Field


class Mensagem(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    messages: list[Mensagem]


class QuizRequest(BaseModel):
    tema: str = Field(min_length=2)
    n: int = Field(default=3, ge=1, le=10)


class AskRequest(BaseModel):
    pergunta: str = Field(min_length=3)
    k: int | None = None


# ETAPA 2 - descreva o formato do quiz com Pydantic:
#   Questao: enunciado (texto), opcoes (lista com exatamente 4 textos),
#            correta (inteiro de 0 a 3) e explicacao (texto).
#   Quiz: questoes (lista com pelo menos 1 Questao).
# Dica: Field(min_length=4, max_length=4) e Field(ge=0, le=3).
class Questao(BaseModel):
    pass


class Quiz(BaseModel):
    pass
