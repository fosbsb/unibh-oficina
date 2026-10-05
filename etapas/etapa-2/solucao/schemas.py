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


class Questao(BaseModel):
    enunciado: str = Field(min_length=1)
    opcoes: list[str] = Field(min_length=4, max_length=4)
    correta: int = Field(ge=0, le=3)
    explicacao: str = Field(min_length=1)


class Quiz(BaseModel):
    questoes: list[Questao] = Field(min_length=1)
