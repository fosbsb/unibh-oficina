# Erros comuns (guia do apoio)

Comece sempre por `docker compose ps` e pelo **selo no topo da página** (http://localhost:8000): ele indica chave, Ollama local e pgvector.

## Ambiente e Docker

| Sintoma | Causa provável | Solução |
|---|---|---|
| `docker compose up` falha com "port is already allocated" | Outro programa usa a porta 8000 | Fechar o programa ou trocar `8000` em `docker-compose.yml` |
| Selo "Ollama local" vermelho | Os modelos ainda estão sendo baixados | `docker compose logs -f ollama-pull` e esperar o `success` |
| `ollama-pull` falha | Sem internet ou disco cheio | Conferir a rede e o espaço; usar o plano B do pendrive (`docs/pre-evento.md`) |
| Selo "pgvector" vermelho | O banco ainda está iniciando ou caiu | `docker compose ps` e `docker compose logs pgvector` |
| Mudou o `.env` e nada mudou | O container só lê o `.env` ao ser criado | `docker compose up -d` (recria o app) |
| Máquina muito lenta/travando | Pouca RAM (menos de 12 GB) | Fechar outros programas; como último recurso, `RERANK_ENABLED=false` |
| Erro de permissão ou arquivos estranhos em `app/` | Pasta com volume do Windows/WSL | Abrir o projeto dentro do WSL ou de uma pasta do usuário |

## Chave e nuvem

| Sintoma | Causa provável | Solução |
|---|---|---|
| "Chave inválida ou ausente" (401) | Chave errada, **cortada** (as chaves têm um ponto no meio) ou o `.env` ainda tem o texto `cole-sua-chave-aqui` | Gerar/copiar a chave inteira em ollama.com e rodar `docker compose up -d` |
| "Limite da conta atingido" (429) | A conta gratuita aceita 1 requisição por vez ou atingiu a cota | Esperar alguns segundos; evitar cliques repetidos; trocar para `gpt-oss:20b` |
| "Modelo não encontrado" (404) | `CHAT_MODEL` com nome errado | Usar um destes: `gpt-oss:20b`, `gpt-oss:120b`, `gemma4:31b`, `nemotron-3-nano:30b`, `nemotron-3-super`, `nemotron-3-ultra` |
| Resposta demora vários segundos para começar | Modelos de raciocínio (`gpt-oss`) "pensam" antes de responder | Normal; esperar |
| "Não consegui falar com um dos serviços" (503) | Sem internet ou serviço local fora do ar | `docker compose ps`; testar a conexão |

## Código do aluno

| Sintoma | Causa provável | Solução |
|---|---|---|
| "Ainda não implementado. Etapa N..." (501) | O stub da etapa ainda lança `NotImplementedError` | Implementar a função indicada na mensagem |
| Teste da etapa falha logo no começo | A etapa anterior não está pronta | `docker compose exec app python scripts/etapa.py preparar N` |
| Aluno muito atrasado | Perdeu tempo em uma etapa | `docker compose exec app python scripts/etapa.py solucao N` (o código dele vai para `app/.backup/`) |
| Quiz: "O modelo não devolveu um quiz válido" | JSON fora do formato 3 vezes seguidas | Reforçar o exemplo no `SISTEMA`; conferir `min_length=4, max_length=4` em `opcoes` |
| `ValidationError` ao criar `Questao` | Campos com nome diferente do JSON | Usar `enunciado`, `opcoes`, `correta`, `explicacao` |
| Streaming aparece de uma vez | `"stream": True` ausente | Conferir o payload em `stream_chat` |
| RAG devolve "Não encontrei isso no material" para tudo | Material não indexado ou `SIM_MIN` alto | Clicar em **Indexar material**; baixar `SIM_MIN` (padrão 0,3) |
| RAG devolve trechos errados | Prefixos dos embeddings omitidos ou índice antigo | Usar `texto_de_pergunta` e `texto_de_trecho`; indexar de novo |
| Erro de dimensão do vetor | A coluna espera 768 dimensões | Conferir `EMBED_MODEL=embeddinggemma:300m` |
| Reranker lento ou com erro | Modelo local pesado para a máquina | `RERANK_ENABLED=false`: o RAG continua só com a busca vetorial |
| No log: "rerank indisponível" | O modelo de reranking não respondeu yes/no | Conferir `RERANK_MODEL=dengcao/Qwen3-Reranker-0.6B:F16`; a variante `Q8_0` gerou texto sem sentido nos testes em Linux arm64 |

## Comandos de diagnóstico

```bash
docker compose ps
docker compose logs --tail 50 app
docker compose exec ollama ollama list
docker compose exec pgvector psql -U postgres -d oficina -c "SELECT count(*) FROM chunks;"
curl http://localhost:8000/health
```
