# Estuda.AI: usando um LLM dentro do seu app

Oficina da UniBH. Em ~4 horas você constrói, etapa por etapa, um assistente de estudos de Banco de Dados que **usa um modelo de linguagem como parte do sistema**: o app chama o modelo por API, valida o que ele devolve e o ancora em um material próprio.

O foco não é usar IA para escrever código. É usar IA **dentro** do código.

| Etapa | Tempo | O que você constrói | Conceito |
|---|---|---|---|
| 0. Setup | 30 min | Ambiente rodando e o primeiro "olá" do modelo | Chave, endpoint, modelo |
| 1. Tutor | 50 min | Chat em streaming com um papel definido | Mensagens, system prompt |
| 2. Quiz | 60 min | Questões geradas em JSON validado | Saída estruturada, validação, retry |
| 3. Material (RAG) | 70 min | Respostas baseadas na apostila, citando a fonte | Embeddings, busca vetorial, grounding |
| 4. Desafio livre | 30 min | Uma extensão sua (sugestão: quiz sobre o material) | Composição |

---

## Como o projeto funciona

```text
Seu navegador ──► app (FastAPI, :8000) ──► Ollama Cloud (chat e JSON, com a sua chave)
                       │
                       ├──► Ollama local (embeddings e reranking)
                       └──► pgvector (Postgres que guarda os vetores)
```

Tudo roda em containers com `docker compose`. Você só edita os arquivos da pasta `app/` no VS Code.

---

## Pré-requisitos

- Docker e Docker Compose funcionando (`docker --version` e `docker compose version`)
- **Pelo menos 12 GB de RAM** na máquina
- VS Code
- Uma conta gratuita em [ollama.com](https://ollama.com) com uma **chave de API** (passo 2 abaixo)
- Cerca de 4 GB livres de disco para as imagens e os modelos locais

## Antes do evento (faça em casa)

Para a oficina não depender do Wi-Fi, baixe tudo antes:

1. Clone ou baixe este repositório e abra a pasta no VS Code.
2. Siga os passos **1 a 3** da seção "Etapa 0" abaixo e confirme que `docker compose up -d` termina sem erro.
3. Confirme que a página http://localhost:8000 abre.

Na primeira vez, o `docker compose up` baixa as imagens e os modelos locais (`embeddinggemma:300m` e `Qwen3-Reranker-0.6B`, cerca de 1,8 GB), e isso demora alguns minutos. Depois disso eles ficam guardados em um volume do Docker.

---

## Etapa 0: Setup e primeiro "olá" (30 min)

### Por que usar o LLM aqui

Antes de qualquer coisa, você precisa entender o contrato: um LLM é um serviço remoto. Seu app envia uma lista de mensagens por HTTP e recebe texto. Nada de mágica: é uma chamada de API como qualquer outra, com autenticação, limites e erros.

### Objetivo

Ambiente de pé e a função `chat_once` devolvendo a resposta do modelo.

### Passo a passo

1. **Crie sua chave.** Entre em [ollama.com](https://ollama.com), vá em *Settings > API keys*, crie uma chave e copie a chave **inteira** (ela tem duas partes separadas por um ponto).
2. **Crie o arquivo `.env`.** Na raiz do projeto, copie o modelo e edite:
   ```bash
   cp .env.example .env
   ```
   Abra o `.env` e troque `cole-sua-chave-aqui` pela sua chave. **Nunca** envie este arquivo para o Git.
3. **Suba o ambiente:**
   ```bash
   docker compose up -d --build
   ```
   Na primeira vez, aguarde os modelos locais serem baixados. Acompanhe com `docker compose logs -f ollama-pull`.
4. **Abra** http://localhost:8000. O selo no canto superior direito mostra o modelo e se há algum problema (chave, Ollama local ou pgvector).
5. **Implemente `chat_once`** em [app/llm.py](app/llm.py), seguindo os comentários do arquivo:
   - monte o `payload` com `model`, `messages` e `stream: False`;
   - envie com `client.post("/api/chat", json=payload)`;
   - chame `check(resp)` e devolva `resp.json()["message"]["content"]`.

### Como verificar

```bash
docker compose exec app pytest etapas/etapa-0 -q
```

Resultado esperado: todos os testes passam (o teste que usa o modelo de verdade só roda se a sua chave estiver no `.env`).

### Se der erro

| Sintoma | O que fazer |
|---|---|
| "Chave inválida" | Confira `OLLAMA_API_KEY` no `.env` e rode `docker compose up -d` de novo para recarregar |
| "Limite da conta atingido" | Aguarde alguns segundos; a conta gratuita aceita 1 requisição por vez |
| Selo "Ollama local" em vermelho | Os modelos ainda estão baixando: `docker compose logs -f ollama-pull` |
| Porta 8000 ocupada | Feche o programa que usa a porta ou troque `8000` em `docker-compose.yml` |

Mais casos em [docs/erros-comuns.md](docs/erros-comuns.md).

### Desafio extra

Troque `CHAT_MODEL` no `.env` por outro modelo (`gpt-oss:120b`, `gemma4:31b`...), reinicie com `docker compose up -d` e compare as respostas.

---

## Etapa 1: Tutor com streaming (50 min)

### Por que usar o LLM aqui

Um aluno pode perguntar a mesma coisa de mil jeitos. Respostas fixas ou regras `if/else` não conseguem explicar o mesmo conceito de formas diferentes conforme a dúvida. O LLM faz isso, e o **system prompt** define o papel e o tom dele sem você programar cada resposta. O **streaming** mostra o texto conforme ele é gerado, o que deixa a espera muito mais agradável.

**Quando não usar:** se a resposta é sempre a mesma (por exemplo, o horário da secretaria), um texto fixo é mais barato, mais rápido e não erra.

### Objetivo

A aba **Tutor** responde em streaming, agindo como tutor de Banco de Dados.

### Passo a passo

1. Abra [app/chat.py](app/chat.py).
2. Escreva o `SYSTEM_PROMPT`: quem o modelo é, em que idioma responde, o que deve e o que não deve fazer (por exemplo, guiar com perguntas em vez de dar a resposta de exercícios).
3. Implemente `stream_chat`:
   - monte o `payload` com `stream: True` e a lista `[system, *messages]`;
   - use `client.stream("POST", "/api/chat", json=payload)`;
   - leia `resp.aiter_lines()`: cada linha é um JSON; entregue `chunk["message"]["content"]` com `yield` e pare quando `chunk["done"]` for verdadeiro.
4. Na aba **Tutor**, pergunte: *"Qual a diferença entre 2FN e 3FN?"*
5. Experimente mudar o `SYSTEM_PROMPT` e perguntar de novo. Veja como o comportamento muda.

### Como verificar

```bash
docker compose exec app pytest etapas/etapa-1 -q
```

### Se der erro

| Sintoma | O que fazer |
|---|---|
| A resposta demora a aparecer | Modelos de raciocínio (como `gpt-oss`) "pensam" antes de responder; espere alguns segundos |
| Erro 501 "Ainda não implementado" | `stream_chat` ainda lança `NotImplementedError`: implemente-a |
| Texto aparece de uma vez | Confira se o payload tem `"stream": True` |

### Desafio extra

Faça o tutor lembrar do que foi dito antes (o histórico já chega em `messages`). Depois, limite o histórico às últimas 6 mensagens e explique por que isso importa (custo e tamanho de contexto).

---

## Etapa 2: Quiz em JSON validado (60 min)

### Por que usar o LLM aqui

Criar questões novas a cada tema é **geração de linguagem**: difícil de fazer com código tradicional. Mas seu app precisa de **dados**, não de texto solto: o front-end espera `enunciado`, 4 `opcoes` e o índice da `correta`. A saída estruturada transforma a resposta do modelo em dado que o app valida. Você nunca deve confiar cegamente na saída de um LLM: valide, e se estiver errada, peça de novo.

**Quando não usar:** se as questões vêm de um banco de questões fixo, uma consulta SQL resolve.

### Objetivo

A aba **Quiz** gera questões e o app só mostra o que passou na validação.

### Passo a passo

1. Abra [app/schemas.py](app/schemas.py) e descreva `Questao` e `Quiz` com Pydantic (enunciado, exatamente 4 opções, `correta` de 0 a 3, explicação). Compare com [etapas/quiz_exemplo.json](etapas/quiz_exemplo.json).
2. Abra [app/quiz.py](app/quiz.py):
   - escreva o `SISTEMA`, pedindo SOMENTE JSON no formato do `Quiz`, com um exemplo;
   - implemente `extrair_json` (modelos às vezes cercam o JSON com texto ou com ` ```json `);
   - implemente `gerar_quiz` com **retry**: se o JSON for inválido, devolva o erro ao modelo e peça a correção (até `QUIZ_MAX_RETRIES` vezes).
3. Na aba **Quiz**, escolha *Índices* e clique em **Gerar quiz**.

### Como verificar

```bash
docker compose exec app pytest etapas/etapa-2 -q
```

Os testes simulam respostas inválidas do modelo, então rodam mesmo sem gastar a cota da nuvem.

### Se der erro

| Sintoma | O que fazer |
|---|---|
| "O modelo não devolveu um quiz válido" | O modelo errou o formato 3 vezes. Reforce o exemplo no `SISTEMA` ou tente outro modelo |
| Erro de validação por `opcoes` | Confira `min_length=4` e `max_length=4` |
| A conta atingiu o limite | A etapa faz até 3 chamadas seguidas no pior caso; aguarde e tente de novo |

### Desafio extra

Experimente o parâmetro `format` da API (um JSON Schema gerado por `Quiz.model_json_schema()`) para forçar o formato na origem. Funciona com o modelo que você escolheu? E se o modelo ignorar o `format`, a sua validação continua protegendo o app?

---

## Etapa 3: Pergunte ao material, o RAG (70 min)

### Por que usar o LLM aqui

O modelo não conhece a apostila da sua turma e, se você perguntar sobre ela, vai **inventar** uma resposta convincente. A técnica de **RAG** resolve isso: o app (1) transforma o material em **embeddings**, vetores que representam o significado do texto, (2) busca os trechos mais parecidos com a pergunta e (3) coloca esses trechos no prompt para o modelo redigir a resposta **citando a fonte**. O LLM só redige a partir do que foi encontrado.

O **reranker** é um segundo modelo, menor, que relê os trechos candidatos e põe à frente os que realmente respondem à pergunta.

**Quando não usar:** para um corpus minúsculo (uma página), basta colocar tudo no prompt. Para dados que mudam a cada segundo ou exigem cálculo exato, use uma consulta SQL.

### Objetivo

A aba **Material** responde com base em `corpus/` e mostra as fontes usadas.

### Passo a passo

1. Leia os arquivos em [corpus/](corpus/): são 5 mini-apostilas de Banco de Dados.
2. Abra [app/rag.py](app/rag.py). O `carregar_chunks` já divide as apostilas em trechos. Implemente, na ordem:
   1. `embed`: `POST /api/embed` no Ollama **local**, com `{"model": ..., "input": [textos]}`;
   2. `ingerir`: gere os embeddings e grave os trechos na tabela `chunks` do pgvector;
   3. `buscar`: o SQL `ORDER BY embedding <=> %s` (distância de cosseno) devolve os mais parecidos;
   4. `rerank` (opcional): o modelo local `Qwen3-Reranker` dá a cada trecho uma nota de 0 a 1 (a probabilidade de ele responder "yes" à pergunta), e você reordena do maior para o menor. Os comentários do arquivo explicam o formato do prompt. Enquanto não fizer, os candidatos ficam na ordem da busca;
   5. `responder`: junte tudo, recuse quando nada for relevante e peça ao modelo da nuvem que responda **só com base nos trechos**, citando `[1]`, `[2]`.
3. Na aba **Material**, clique em **Indexar material** e pergunte: *"Quando um índice pode deixar o banco mais lento?"*
4. Pergunte algo fora do material (*"Qual a capital da França?"*): o app deve dizer que não encontrou, sem chamar o modelo.
5. Veja no terminal (`docker compose logs -f app`) as notas de similaridade de cada trecho.

### Como verificar

```bash
docker compose exec app pytest etapas/etapa-3 -q
```

O teste mede se, em pelo menos 8 de 10 perguntas, o trecho certo aparece entre os recuperados.

### Se der erro

| Sintoma | O que fazer |
|---|---|
| "Não consegui falar com um dos serviços" | `docker compose ps`: veja se `ollama` e `pgvector` estão saudáveis |
| Busca devolve vazio | Clique em **Indexar material** antes de perguntar |
| "Não encontrei isso no material" para tudo | O limiar `SIM_MIN` do `.env` está alto demais; baixe e compare |
| Reranker lento ou falhando | Coloque `RERANK_ENABLED=false` no `.env`: o RAG continua funcionando só com a busca |

### Desafio extra

Compare os resultados com e sem o reranker (`RERANK_ENABLED`). Em quais perguntas a ordem dos trechos muda? E rode a consulta SQL de similaridade direto no banco:

```bash
docker compose exec pgvector psql -U postgres -d oficina -c "SELECT fonte, titulo FROM chunks LIMIT 5;"
```

---

## Etapa 4: Desafio livre (30 min)

Use o que construiu para criar algo seu. A rota `GET /extra/ping` em [app/extra.py](app/extra.py) já está incluída no app: acrescente suas rotas ali.

Sugestão: um **quiz sobre o material**. Receba um tema, recupere os trechos com `embed`, `buscar` e `rerank`, passe-os como `contexto` para `gerar_quiz` e devolva as questões. Outras ideias: resumir um arquivo do corpus, gerar flashcards, avaliar a resposta escrita de um aluno.

Verifique com `docker compose exec app pytest etapas/etapa-4 -q`.

---

## Se você ficou para trás

Você não precisa terminar uma etapa para seguir. Dois comandos resolvem:

```bash
# prepara o app no ponto de partida da etapa 3 (aplica as soluções das etapas 0, 1 e 2)
docker compose exec app python scripts/etapa.py preparar 3

# aplica a solução da etapa 2 (e das anteriores)
docker compose exec app python scripts/etapa.py solucao 2
```

O seu código anterior é guardado em `app/.backup/` antes de ser substituído.

## Comandos úteis

| Comando | Para quê |
|---|---|
| `docker compose up -d --build` | Subir (ou atualizar) o ambiente |
| `docker compose ps` | Ver o estado dos serviços |
| `docker compose logs -f app` | Acompanhar o log do app |
| `docker compose down` | Parar tudo (os dados ficam nos volumes) |
| `docker compose exec app pytest etapas/etapa-N -q` | Testar a etapa N |

## Estrutura do projeto

```text
app/            seu código (os arquivos com "ETAPA" nos comentários são os seus exercícios)
  static/       a tela (HTML pronto)
corpus/         as apostilas usadas pelo RAG
etapas/         soluções de referência, testes e perguntas de verificação
scripts/        etapa.py: prepara ou aplica uma etapa
docs/           material do instrutor e do apoio
docker-compose.yml, .env.example, db/init.sql
```

## Segurança e privacidade

- A chave de API é pessoal: não a compartilhe e não a envie ao Git.
- O que você digita no app vai para o ollama.com: **não escreva dados pessoais** durante a oficina.
- A senha do banco (`oficina`) serve só para este ambiente local. Não reutilize este arranjo em produção.
