from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(extra="ignore")

    ollama_api_key: str = ""
    chat_model: str = "gpt-oss:20b"
    embed_model: str = "embeddinggemma:300m"
    rerank_model: str = "dengcao/Qwen3-Reranker-0.6B:F16"
    rerank_enabled: bool = True

    ollama_cloud_url: str = "https://ollama.com"
    ollama_local_url: str = "http://ollama:11434"
    database_url: str = "postgresql://postgres:oficina@pgvector:5432/oficina"

    quiz_max_retries: int = 2
    rag_top_k: int = 4
    sim_min: float = 0.3


settings = Settings()
