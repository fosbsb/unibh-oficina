# Checklist antes do evento

Para a etapa 0 caber em 30 minutos, o maior risco é a rede: 30 pessoas baixando imagens e modelos no mesmo Wi-Fi. Resolva isso antes.

## Para cada aluno (1 semana antes)

- [ ] Criou a conta gratuita em [ollama.com](https://ollama.com) e uma **chave de API** (Settings > API keys).
- [ ] Copiou a chave **inteira**, incluindo tudo o que vem depois do ponto (as chaves têm o formato `parte1.parte2`). Uma chave cortada devolve erro 401.
- [ ] Docker e Docker Compose funcionando; máquina com **12 GB de RAM** ou mais.
- [ ] Clonou o repositório, criou o `.env` (`cp .env.example .env`) e colou a chave.
- [ ] Rodou `docker compose up -d --build` e esperou terminar (baixa cerca de 3 GB na primeira vez).
- [ ] Abriu http://localhost:8000 e o selo no topo está verde.

## Tamanho dos downloads (medido)

| Item | Tamanho aproximado |
|---|---|
| `embeddinggemma:300m` | 621 MB |
| `dengcao/Qwen3-Reranker-0.6B:F16` | 1,2 GB |
| Imagens Docker (ollama, pgvector, python) | cerca de 1,5 GB |

## Plano B: levar tudo em pendrive (instrutor)

Em uma máquina que já está com tudo funcionando:

```bash
# imagens
docker save ollama/ollama pgvector/pgvector:pg16 python:3.12-slim -o imagens.tar

# modelos locais (volume ollama_models)
docker run --rm -v unibh-oficina_ollama_models:/dados -v "$PWD":/saida alpine \
  tar czf /saida/modelos-ollama.tgz -C /dados .
```

Na máquina do aluno:

```bash
docker load -i imagens.tar
docker volume create unibh-oficina_ollama_models
docker run --rm -v unibh-oficina_ollama_models:/dados -v "$PWD":/entrada alpine \
  tar xzf /entrada/modelos-ollama.tgz -C /dados
docker compose up -d --build
```

O nome do volume depende do nome da pasta do projeto (`unibh-oficina_ollama_models` quando a pasta se chama `unibh-oficina`). Confira com `docker volume ls`.

## Para o instrutor, na véspera

- [ ] Rodou o fluxo completo com uma chave real: etapas 0 a 4 e `docker compose exec app pytest -q`.
- [ ] Confirmou que os 6 modelos de nuvem respondem na conta free (`gpt-oss:20b` é o padrão).
- [ ] Testou `python scripts/etapa.py solucao 4` e `preparar 3` para saber o que o aluno verá.
- [ ] Imprimiu ou projetou [docs/erros-comuns.md](erros-comuns.md) para o apoio.
- [ ] Combinou com o apoio quem atende qual fileira da sala.
