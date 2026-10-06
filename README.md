<div align="center">

# Oficina IA da UniBH - Tecnisys

**Estuda.AI: usando um LLM dentro do seu app**

![Oficina](https://img.shields.io/badge/oficina-UniBH%202026-1e3a8a?style=flat-square)
![Duração](https://img.shields.io/badge/dura%C3%A7%C3%A3o-4h-0ea5e9?style=flat-square)
![Nível](https://img.shields.io/badge/n%C3%ADvel-iniciante%20a%20intermedi%C3%A1rio-64748b?style=flat-square)
![Licença MIT](https://img.shields.io/badge/licen%C3%A7a-MIT-22c55e?style=flat-square)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-fosbsb-0A66C2?style=flat-square)](https://www.linkedin.com/in/fosbsb/)

**IA**

![LLM](https://img.shields.io/badge/LLM-API%20de%20chat-7c3aed?logo=openai&logoColor=white&style=flat-square)
![Ollama](https://img.shields.io/badge/Ollama-Cloud%20%2B%20local-000000?logo=ollama&logoColor=white&style=flat-square)
![RAG](https://img.shields.io/badge/RAG-busca%20vetorial-16a34a?style=flat-square)
![Embeddings](https://img.shields.io/badge/embeddings-768%20dim-f59e0b?style=flat-square)
![Reranker](https://img.shields.io/badge/reranker-Qwen3-ea580c?style=flat-square)
![Saída estruturada](https://img.shields.io/badge/sa%C3%ADda-JSON%20validado-db2777?style=flat-square)

**Desenvolvimento**

![Python](https://img.shields.io/badge/Python-3.12-3776ab?logo=python&logoColor=white&style=flat-square)
![FastAPI](https://img.shields.io/badge/FastAPI-async-009688?logo=fastapi&logoColor=white&style=flat-square)
![Pydantic](https://img.shields.io/badge/Pydantic-v2-e92063?logo=pydantic&logoColor=white&style=flat-square)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16%20%2B%20pgvector-4169e1?logo=postgresql&logoColor=white&style=flat-square)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ed?logo=docker&logoColor=white&style=flat-square)
![pytest](https://img.shields.io/badge/testes-pytest-0a9edc?logo=pytest&logoColor=white&style=flat-square)
![Ruff](https://img.shields.io/badge/lint-Ruff-d7ff64?logo=ruff&logoColor=black&style=flat-square)

</div>

---

Em 4 horas, você constrói o **Estuda.AI**, um assistente de estudos da disciplina de Banco de Dados. Etapa por etapa, o app passa a chamar um modelo de linguagem por API, validar o que ele devolve e responder com base em um material próprio, citando a fonte.

O foco não é usar IA para escrever código. É usar IA **dentro** do código.

> [!NOTE]
> **Sobre o nome.** "Estuda.AI" é apenas um **nome fictício**, criado para esta oficina. Ele **não tem relação** com nenhum produto, serviço, empresa ou marca existente, e qualquer semelhança é mera coincidência. O projeto é **material didático**, sem fins comerciais.

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
┌─────────────────────────┐         ┌─────────────────────────┐         ┌─────────────────────────┐
│ SEU NAVEGADOR           │         │ APP (FastAPI)           │         │ OLLAMA CLOUD            │
│                         │   HTTP  │                         │  HTTPS  │                         │
│ a tela do Estuda.AI     │  ────►  │ o código que você       │  ────►  │ chat, quiz e respostas  │
│ em localhost:8000       │         │ escreve em app/         │         │ usa a sua chave         │
│                         │         │ porta 8000              │         │ na internet             │
└─────────────────────────┘         └─────────────────────────┘         └─────────────────────────┘
                                                 │
                                  ┌──────────────┴─────────────────┐
                                  ▼                                ▼
                     ┌─────────────────────────┐      ┌─────────────────────────┐
                     │ OLLAMA LOCAL            │      │ PGVECTOR (Postgres 16)  │
                     │                         │      │                         │
                     │ embeddings e reranking  │      │ trechos e vetores       │
                     │ modelos baixados        │      │ da apostila             │
                     │ container               │      │ container               │
                     └─────────────────────────┘      └─────────────────────────┘
```

| Caixa | O que faz | Onde roda | Etapa |
|---|---|---|---|
| **Seu navegador** | Mostra a tela do Estuda.AI (abas Conexão, Tutor, Quiz e Material) | Sua máquina | todas |
| **App (FastAPI)** | O código que você escreve em `app/`: monta as mensagens, valida as respostas e orquestra tudo | Container `app` | 0 a 4 |
| **Ollama Cloud** | O modelo de linguagem que conversa, gera o quiz e redige as respostas (usa a sua chave) | Internet (ollama.com) | 0, 1, 2 e 3 |
| **Ollama local** | Transforma textos em vetores (embeddings) e reordena os trechos (reranking) | Container `ollama` | 3 |
| **pgvector** | Guarda os trechos da apostila e os vetores, e busca os mais parecidos com a pergunta | Container `pgvector` | 3 |

O app, o Ollama local e o pgvector sobem juntos, em containers, com um único `docker compose`; o navegador é o seu e o Ollama Cloud fica na internet. Você só edita os arquivos da pasta `app/` no VS Code.

---

## Pré-requisitos

- Docker e Docker Compose funcionando (`docker --version` e `docker compose version`)
- **Pelo menos 12 GB de RAM** na máquina
- VS Code
- Uma conta gratuita em [ollama.com](https://ollama.com) com uma **chave de API** (passo 2 abaixo)
- Pelo menos 10 GB livres de disco para as imagens e os modelos locais
- [Git](https://git-scm.com/downloads) (opcional: serve para clonar; sem ele, baixe o ZIP)

### Baixe o projeto

O código está em **https://github.com/fosbsb/unibh-oficina**. Escolha uma das duas formas.

**Opção 1: clonar com Git** (recomendada)

```bash
git clone https://github.com/fosbsb/unibh-oficina.git
cd unibh-oficina
```

**Opção 2: baixar o ZIP** (sem Git)

1. Abra o link acima, clique no botão verde **Code** e depois em **Download ZIP** (ou baixe direto de [main.zip](https://github.com/fosbsb/unibh-oficina/archive/refs/heads/main.zip)).
2. Extraia o arquivo. Será criada a pasta `unibh-oficina-main`.

Nas duas formas, abra a **pasta do projeto** no VS Code (*File > Open Folder*) e use o terminal dessa pasta para os comandos deste README.

---

## Etapa 0: Setup e primeiro "olá" (30 min)

### Por que usar o LLM aqui

Antes de qualquer coisa, você precisa entender o contrato: um LLM é um serviço remoto. Seu app envia uma lista de mensagens por HTTP e recebe texto. Nada de mágica: é uma chamada de API como qualquer outra, com autenticação, limites e erros.

### Objetivo

Ambiente no ar e a função `chat_once` devolvendo a resposta do modelo, que você vai ver na aba **Conexão** da tela.

### Passo a passo

1. **Crie sua chave.** Entre em [ollama.com](https://ollama.com), vá em *Settings > API keys*, crie uma chave e copie a chave **inteira**.

   > [!NOTE]
   > **Como é a chave:** ela tem **57 caracteres**, em duas partes separadas por **um ponto (`.`)**: **32** caracteres, o ponto e mais **24**.
   >
   > ```text
   > xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx.xxxxxxxxxxxxxxxxxxxxxxxx
   > ```
   >
   > Se faltar a parte depois do ponto, a chave está cortada e o app mostrará o erro 401 ("Chave inválida").

   > [!TIP]
   > **Acompanhe o seu uso.** Os modelos de nuvem consomem a cota **gratuita** da sua conta (*Included usage*), que se renova periodicamente (a tela mostra "Resets in…"). Em [ollama.com/settings](https://ollama.com/settings) você vê quanto já usou, quando a cota renova e quais modelos você chamou. A conta gratuita só aceita estes modelos de nuvem: `gpt-oss:20b`, `gpt-oss:120b`, `gemma4:31b`, `nemotron-3-nano:30b`, `nemotron-3-super` e `nemotron-3-ultra`. A oficina usa o `gpt-oss:20b`.
   >
   > No exemplo abaixo, 92 requisições ao `gpt-oss:20b` consumiram só 0,4% da cota gratuita, o que dá uma ideia do tamanho do consumo da oficina.

   ![Página Included usage em ollama.com/settings: modelos gratuitos, porcentagem de uso, renovação da cota e requisições por modelo](docs/img/ollama-uso.png)

2. **Crie o arquivo `.env`.** Na raiz do projeto, copie o modelo e edite:
   ```bash
   cp .env.example .env
   ```
   Abra o `.env` e troque `cole-sua-chave-aqui` pela sua chave, no formato acima e sem espaços nem aspas (`OLLAMA_API_KEY=sua-chave-inteira`). **Nunca** envie este arquivo para o Git.
3. **Suba o ambiente:**
   ```bash
   docker compose up -d --build
   ```
   Na primeira vez, o comando **só devolve o prompt depois que os modelos locais (~1,8 GB) terminam de baixar**, o que levou cerca de 8 minutos em uma conexão comum: não é travamento. Para acompanhar, abra **outro terminal** e rode `docker compose logs -f ollama-pull` (termina com `success`).

   Quando terminar, a saída termina com `Healthy` para `ollama` e `pgvector`, `Exited` para `ollama-pull` (ele só baixa os modelos e sai) e `Started` para `app`, como no exemplo abaixo (aqui as imagens já estavam em cache, por isso foi rápido):

   ![Saída do docker compose up -d --build com todos os serviços no ar](docs/img/docker-compose-up.png)

   Para conferir que tudo está no ar, liste os containers:

   ```bash
   docker ps
   ```

   Você deve ver os três (`app`, `pgvector` e `ollama`), com `Up` e `(healthy)` nos dois últimos:

   ```text
   CONTAINER ID   IMAGE                    COMMAND                  CREATED          STATUS                    PORTS                      NAMES
   60842ac0681a   unibh-oficina-app        "uvicorn app.main:ap…"   20 seconds ago   Up 11 seconds             127.0.0.1:8000->8000/tcp   unibh-oficina-app-1
   a828fff04c52   pgvector/pgvector:pg16   "docker-entrypoint.s…"   20 seconds ago   Up 20 seconds (healthy)   5432/tcp                   unibh-oficina-pgvector-1
   2eddc309ce6d   ollama/ollama            "/bin/ollama serve"      20 seconds ago   Up 20 seconds (healthy)   11434/tcp                  unibh-oficina-ollama-1
   ```

4. **Abra** http://localhost:8000. O selo no canto superior direito mostra o modelo e se há algum problema (chave, Ollama local ou pgvector).
5. **Entre no container e veja a chamada de API "na mão" com `curl`.** O container `app` já tem `curl` e `jq` instalados, e a sua chave já está no ambiente dele (vem do `.env`): você não precisa instalar nada nem fazer `export`. Entre nele:
   ```bash
   docker compose exec app bash
   ```
   O prompt muda para algo como `root@abc123:/workspace#`: tudo o que você digitar agora roda **dentro do container** (para sair, digite `exit`). Confirme que a chave chegou; o comando mostra só o tamanho, sem revelar a chave:
   ```bash
   echo ${#OLLAMA_API_KEY}
   ```
   Deve aparecer `57`. Se aparecer `0`, a chave não chegou; se for outro número, a chave está cortada ou com texto a mais: confira o `.env` e rode `docker compose up -d` (fora do container). Agora faça, "na mão" (dentro do container), a mesma chamada que o app fará. O `| jq` deixa o JSON legível:
   ```bash
   curl -s https://ollama.com/api/chat \
     -H "Authorization: Bearer $OLLAMA_API_KEY" \
     -d '{
       "model": "gpt-oss:20b",
       "stream": false,
       "messages": [{"role": "user", "content": "Responda apenas: ok"}]
     }' | jq
   ```
   A resposta tem esta forma (resumida), e o texto está em `message.content`:
   ```json
   {
     "model": "gpt-oss:20b",
     "message": { "role": "assistant", "content": "ok", "thinking": "..." },
     "done": true
   }
   ```
   Para mostrar só o texto, troque o final por `| jq -r '.message.content'`. Agora troque `$OLLAMA_API_KEY` por `chave-errada` e repita (sem o `jq`): a nuvem devolve `{"error":"Unauthorized"}`. É esse erro 401 que o app traduz para "Chave inválida". Veja também o estado do app, que roda neste mesmo container:
   ```bash
   curl -s http://localhost:8000/health | jq
   ```

   > [!IMPORTANT]
   > **Todos os `curl` deste README rodam dentro do container.** Sempre que abrir um terminal novo, entre de novo com `docker compose exec app bash`. Como o container é Linux, os comandos são iguais no Windows, no macOS e no Linux, sem `export` e sem problemas de aspas no PowerShell. O `pytest` também pode ser rodado lá dentro, sem o prefixo `docker compose exec app`.

6. **Implemente `chat_once`** em [app/llm.py](app/llm.py), seguindo os comentários do arquivo:
   - monte o `payload` com `model`, `messages` e `stream: False`;
   - envie com `client.post("/api/chat", json=payload)`;
   - chame `check(resp)` e devolva `resp.json()["message"]["content"]`.

### Como verificar

Faça as três verificações, nesta ordem. Se uma falhar, corrija antes de seguir.

#### 1. Pela linha de comando

```bash
docker compose exec app pytest etapas/etapa-0
```

Todos os testes devem terminar em `PASSED`, com a linha final `N passed`. Cada teste imprime o que fez (o corpo enviado, a resposta recebida). O teste que usa o modelo de verdade só roda se a sua chave estiver no `.env`.

Assim aparece quando está tudo certo (5 testes `PASSED`):

![Saída do pytest da etapa 0 com os 5 testes passando](docs/img/pytest-etapa-0.png)

#### 2. Pelo `curl`

Dentro do container (`docker compose exec app bash`), chame o endpoint `/hello`, que usa o seu `chat_once`:

```bash
curl -s -X POST http://localhost:8000/hello \
  -H "Content-Type: application/json" \
  -d '{"mensagem":"Responda apenas: ok"}' | jq
```

Resultado esperado:

```json
{
  "modelo": "gpt-oss:20b",
  "resposta": "ok"
}
```

Se ainda não implementou `chat_once`, o `curl` mostra `{"erro":"Ainda não implementado. Etapa 0: ..."}`.

#### 3. Pela interface

1. Abra http://localhost:8000. O selo no canto superior direito deve estar **verde** (`gpt-oss:20b · Ollama Cloud`).
2. Fique na aba **Conexão**, deixe ou troque a mensagem e clique em **Testar conexão**.
3. Deve aparecer um cartão **"RESPOSTA DE gpt-oss:20b"** com o texto do modelo.

Se, em vez disso, aparecer uma faixa vermelha, leia a mensagem: "Chave inválida" (confira o `.env`), "Limite da conta atingido" (espere alguns segundos) ou "Ainda não implementado" (falta o `chat_once`).

![Etapa 0 na interface: aba Conexão, mensagem digitada e resposta do modelo](docs/img/etapa-0.gif)

### Se der erro

| Sintoma | O que fazer |
|---|---|
| "Chave inválida" | Confira `OLLAMA_API_KEY` no `.env` e rode `docker compose up -d` de novo para recarregar |
| "Limite da conta atingido" | Aguarde alguns segundos; a conta gratuita aceita 1 requisição por vez |
| Selo "Ollama local" em vermelho | Os modelos ainda estão baixando: `docker compose logs -f ollama-pull` |
| Porta 8000 ocupada | Feche o programa que usa a porta ou troque `8000` em `docker-compose.yml` |
| `curl: command not found` ou `jq: command not found` | A imagem do app é antiga: saia do container e rode `docker compose up -d --build` |
| `echo ${#OLLAMA_API_KEY}` mostra `0` | A chave não chegou ao container: confira o `.env` e rode `docker compose up -d` |
| `echo ${#OLLAMA_API_KEY}` não mostra `57` | A chave está cortada ou tem espaço/aspas: copie de novo a chave inteira (32 + `.` + 24) |

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

### Experimente com curl

> [!NOTE]
> Rode estes comandos **dentro do container** (`docker compose exec app bash`), onde `curl`, `jq` e a chave já estão disponíveis.

Com `"stream": true`, a nuvem devolve **uma linha JSON por pedaço de texto**. O `-N` desliga o buffer do `curl` para você ver os pedaços chegando, e o `system` define o papel do modelo:

```bash
curl -N https://ollama.com/api/chat \
  -H "Authorization: Bearer $OLLAMA_API_KEY" \
  -d '{
    "model": "gpt-oss:20b",
    "stream": true,
    "messages": [
      {"role": "system", "content": "Você é um tutor de Banco de Dados. Responda em uma frase."},
      {"role": "user", "content": "O que é uma chave primária?"}
    ]
  }'
```

Cada linha tem este formato, e o texto está em `message.content`; a última traz `"done":true`:

```json
{"model":"gpt-oss:20b","message":{"role":"assistant","content":" chave"},"done":false}
```

O `gpt-oss` "pensa" antes de responder: as primeiras linhas trazem `"content":""` e o raciocínio em `"thinking"`. É exatamente isso que o seu `stream_chat` vai ler, linha por linha.

#### Quero ver a resposta inteira, não em pedaços

A resposta chega "quebrada" porque `"stream": true` manda um pedaço por linha. Há duas saídas:

**1. Streaming, mas juntando os pedaços em um texto só:** você vê a resposta se formando, sem as linhas JSON. O `-j` do `jq` não quebra a linha entre os pedaços, e linhas sem texto não imprimem nada:

```bash
curl -s -N https://ollama.com/api/chat \
  -H "Authorization: Bearer $OLLAMA_API_KEY" \
  -d '{"model":"gpt-oss:20b","stream":true,"messages":[{"role":"user","content":"O que é uma chave primária? Uma frase."}]}' \
  | jq -rj '.message.content'
```

**2. Sem streaming:** com `"stream": false` a nuvem espera terminar e devolve **um único JSON** com a resposta completa. O `jq -r` mostra só o texto (`-r` tira as aspas):

```bash
curl -s https://ollama.com/api/chat \
  -H "Authorization: Bearer $OLLAMA_API_KEY" \
  -d '{"model":"gpt-oss:20b","stream":false,"messages":[{"role":"user","content":"O que é uma chave primária? Uma frase."}]}' \
  | jq -r '.message.content'
```

Sem o `| jq ...` no final, você vê o JSON inteiro, com `thinking`, tempos e contagem de tokens.

### Passo a passo

1. Abra [app/chat.py](app/chat.py).
2. Escreva o `SYSTEM_PROMPT`: quem o modelo é, em que idioma responde, o que deve e o que não deve fazer (por exemplo, guiar com perguntas em vez de dar a resposta de exercícios). Peça também resposta em **texto corrido, sem Markdown**, e curta (na seção "Desafio extra" abaixo você ativa o Markdown).
3. Implemente `stream_chat`:
   - monte o `payload` com `stream: True` e a lista `[system, *messages]`;
   - use `client.stream("POST", "/api/chat", json=payload)`;
   - leia `resp.aiter_lines()`: cada linha é um JSON; entregue `chunk["message"]["content"]` com `yield` e pare quando `chunk["done"]` for verdadeiro.
4. Na aba **Tutor**, pergunte: *"Qual a diferença entre 2FN e 3FN?"*
5. Experimente mudar o `SYSTEM_PROMPT` e perguntar de novo. Veja como o comportamento muda.

### Como verificar

#### 1. Pela linha de comando

```bash
docker compose exec app pytest etapas/etapa-1
```

Todos os testes devem terminar em `PASSED`. Eles simulam a nuvem para checar o streaming, o system prompt e os erros (401 e 429); o teste com o modelo real roda se a chave estiver no `.env`.

#### 2. Pelo `curl`

Dentro do container, chame o **seu** endpoint, que repassa o streaming da nuvem:

```bash
curl -N -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"messages":[{"role":"user","content":"O que é uma chave primária? Uma frase."}]}'
```

O resultado é o texto da resposta, chegando aos poucos.

#### 3. Pela interface

1. Abra http://localhost:8000 e entre na aba **Tutor**.
2. Pergunte: *"Qual a diferença entre 2FN e 3FN?"* e clique em **Enviar**.
3. A resposta deve aparecer **em texto corrido**, no papel de tutor (explica e, em geral, termina com uma pergunta que guia você). Enquanto o modelo responde, o botão fica desabilitado.
4. Mude o `SYSTEM_PROMPT` (por exemplo, "responda como um pirata"), salve e pergunte de novo: o tom da resposta deve mudar sem você mexer em mais nada.

![Etapa 1 na interface: aba Tutor com a pergunta e a resposta do tutor](docs/img/etapa-1.gif)

### Se der erro

| Sintoma | O que fazer |
|---|---|
| A resposta demora a aparecer | Modelos de raciocínio (como `gpt-oss`) "pensam" antes de responder; espere alguns segundos |
| Erro 501 "Ainda não implementado" | `stream_chat` ainda lança `NotImplementedError`: implemente-a |
| Texto aparece de uma vez | Confira se o payload tem `"stream": True` |

### Desafio extra

**Markdown na resposta.** A tela do Tutor já sabe **renderizar Markdown** (negrito, listas, tabelas e blocos de código). Ajuste o `SYSTEM_PROMPT` para o tutor responder em Markdown (por exemplo, listas para comparar conceitos e blocos ```` ```sql ```` para código), pergunte de novo e veja a diferença na tela.

Faça o tutor lembrar do que foi dito antes (o histórico já chega em `messages`). Depois, limite o histórico às últimas 6 mensagens e explique por que isso importa (custo e tamanho de contexto).

> [!NOTE]
> **Como limitar as mensagens.** O navegador envia o histórico inteiro a cada pergunta, então o corte é feito em `stream_chat`, ao montar o `payload`. Use uma fatia da lista em vez de `messages` inteira:
>
> ```python
> ULTIMAS = 6
> recentes = messages[-ULTIMAS:]
> payload = {
>     "model": settings.chat_model,
>     "stream": True,
>     "messages": [{"role": "system", "content": SYSTEM_PROMPT}, *recentes],
> }
> ```
>
> - O `SYSTEM_PROMPT` fica **fora** do corte: ele vai sempre, no início, senão o tutor perde o papel quando a conversa cresce.
> - Como a lista termina na pergunta atual (`user`), uma fatia de tamanho par pode começar numa resposta do `assistant`. Se isso incomodar, descarte a primeira mensagem quando ela não for do `user`.
> - Por que importa: cada chamada reenvia o histórico, e o modelo cobra e limita por **tokens**. Menos mensagens deixam a resposta mais rápida e barata, e evitam estourar a janela de contexto, ao custo de o tutor esquecer o começo da conversa.

---

## Etapa 2: Quiz em JSON validado (60 min)

### Por que usar o LLM aqui

Criar questões novas a cada tema é **geração de linguagem**: difícil de fazer com código tradicional. Mas seu app precisa de **dados**, não de texto solto: o front-end espera `enunciado`, 4 `opcoes` e o índice da `correta`. A saída estruturada transforma a resposta do modelo em dado que o app valida. Você nunca deve confiar cegamente na saída de um LLM: valide, e se estiver errada, peça de novo.

**Quando não usar:** se as questões vêm de um banco de questões fixo, uma consulta SQL resolve.

### Objetivo

A aba **Quiz** gera questões e o app só mostra o que passou na validação.

### Experimente com curl

> [!NOTE]
> Rode dentro do container (`docker compose exec app bash`).

Para a nuvem, um quiz é só uma conversa em que o `system` exige JSON. O primeiro `jq` extrai o texto da resposta, e o segundo tenta **ler esse texto como JSON** e formatá-lo:

```bash
curl -s https://ollama.com/api/chat \
  -H "Authorization: Bearer $OLLAMA_API_KEY" \
  -d '{
    "model": "gpt-oss:20b",
    "stream": false,
    "messages": [
      {"role": "system", "content": "Responda SOMENTE com JSON no formato {\"questoes\":[{\"enunciado\":\"...\",\"opcoes\":[\"A\",\"B\",\"C\",\"D\"],\"correta\":0,\"explicacao\":\"...\"}]}"},
      {"role": "user", "content": "Gere 1 questão sobre índices."}
    ]
  }' | jq -r '.message.content' | jq
```

O modelo devolve o JSON dentro de `message.content`, como uma **string**: é por isso que são dois `jq`. Se o modelo escrever qualquer texto fora do JSON (por exemplo, "Claro! Aqui está:" ou cercas ` ```json `), o segundo `jq` reclama de `parse error`. É exatamente esse erro que o seu código precisa tratar. Repare também que o modelo pode errar o formato (colocar `A)` dentro das opções ou usar mais de 4): por isso existem a validação com Pydantic e o retry.

### Passo a passo

1. Abra [app/schemas.py](app/schemas.py) e descreva `Questao` e `Quiz` com Pydantic (enunciado, exatamente 4 opções, `correta` de 0 a 3, explicação). Compare com [etapas/quiz_exemplo.json](etapas/quiz_exemplo.json).
2. Abra [app/quiz.py](app/quiz.py):
   - escreva o `SISTEMA`, pedindo SOMENTE JSON no formato do `Quiz`, com um exemplo;
   - implemente `extrair_json` (modelos às vezes cercam o JSON com texto ou com ` ```json `);
   - implemente `gerar_quiz` com **retry**: se o JSON for inválido, devolva o erro ao modelo e peça a correção (até `QUIZ_MAX_RETRIES` vezes).
3. Na aba **Quiz**, escolha *Índices* e clique em **Gerar quiz**.

### Como verificar

#### 1. Pela linha de comando

```bash
docker compose exec app pytest etapas/etapa-2
```

Todos os testes devem terminar em `PASSED`. Eles simulam respostas inválidas do modelo, então rodam mesmo sem gastar a cota da nuvem.

#### 2. Pelo `curl`

Dentro do container, chame o **seu** endpoint. Ele já devolve o quiz validado, não mais texto solto:

```bash
curl -s -X POST http://localhost:8000/quiz \
  -H "Content-Type: application/json" \
  -d '{"tema":"Índices","n":1}' | jq
```

O resultado é um JSON com `questoes`, cada uma com `enunciado`, 4 `opcoes`, `correta` (0 a 3) e `explicacao`.

#### 3. Pela interface

1. Abra http://localhost:8000 e entre na aba **Quiz**.
2. Deixe o tema *Índices* e 3 questões e clique em **Gerar quiz**.
3. Devem aparecer **3 cartões**, cada um com um enunciado e **exatamente 4 opções**.
4. Clique em uma opção: a **correta fica verde**, a errada (se você errou) fica vermelha e aparece a **explicação**.
5. Se aparecer "O modelo não devolveu um quiz válido", o modelo errou o formato 3 vezes seguidas: reforce o exemplo no `SISTEMA` e tente de novo.

![Etapa 2 na interface: aba Quiz com as questões geradas e a resposta corrigida](docs/img/etapa-2.gif)

### Se der erro

| Sintoma | O que fazer |
|---|---|
| "O modelo não devolveu um quiz válido" | O modelo errou o formato 3 vezes. Reforce o exemplo no `SISTEMA` ou tente outro modelo |
| Erro de validação por `opcoes` | Confira `min_length=4` e `max_length=4` |
| A conta atingiu o limite | A etapa faz até 3 chamadas seguidas no pior caso; aguarde e tente de novo |

---

## Etapa 3: Pergunte ao material, o RAG (70 min)

### Por que usar o LLM aqui

O modelo não conhece a apostila da sua turma e, se você perguntar sobre ela, vai **inventar** uma resposta convincente. A técnica de **RAG** resolve isso: o app (1) transforma o material em **embeddings**, vetores que representam o significado do texto, (2) busca os trechos mais parecidos com a pergunta e (3) coloca esses trechos no prompt para o modelo redigir a resposta **citando a fonte**. O LLM só redige a partir do que foi encontrado.

O **reranker** é um segundo modelo, menor, que relê os trechos candidatos e põe à frente os que realmente respondem à pergunta.

**Quando não usar:** para um corpus minúsculo (uma página), basta colocar tudo no prompt. Para dados que mudam a cada segundo ou exigem cálculo exato, use uma consulta SQL.

### Objetivo

A aba **Material** responde com base em `corpus/` e mostra as fontes usadas.

### Visão geral: o caminho dos dados

O RAG tem duas fases. Os números das caixas são os mesmos do **Passo a passo** abaixo.

**Fase 1: indexar o material** (uma vez, ao clicar em **Indexar material**). O app transforma cada trecho da apostila em um vetor e guarda no pgvector.

```text
┌────────────────┐   ┌───────────────────┐   ┌───────────────────────┐   ┌───────────────────────┐
│ corpus/*.md    │   │ carregar_chunks   │   │ 1. embed              │   │ 2. ingerir            │
│                │──►│ divide em trechos │──►│ Ollama local          │──►│ grava os trechos e    │
│ 5 apostilas    │   │ (23 trechos)      │   │ texto → 768 números   │   │ vetores no pgvector   │
└────────────────┘   └───────────────────┘   └───────────────────────┘   └───────────────────────┘
```

**Fase 2: responder uma pergunta** (a cada pergunta na aba **Material**). O app acha os trechos mais parecidos, confere se são relevantes e só então chama o modelo da nuvem.

```text
 "Quando um índice pode deixar o banco mais lento?"
                              │
                              ▼
┌────────────────────────────────────────────────────────┐
│ 1. embed  (Ollama local)                               │
│ a pergunta vira um vetor de 768 números                │
└─────────────────────────────┬──────────────────────────┘
                              │
                              ▼
┌────────────────────────────────────────────────────────┐
│ 3. buscar  (pgvector)                                  │
│ ORDER BY embedding <=> vetor  LIMIT k                  │
│ devolve os k trechos mais parecidos                    │
└─────────────────────────────┬──────────────────────────┘
                              │
                              ▼
┌────────────────────────────────────────────────────────┐
│ 4. rerank  (Ollama local, opcional)                    │
│ nota de 0 a 1 por trecho: P(yes) / (P(yes) + P(no))    │
│ reordena do maior para o menor                         │
└─────────────────────────────┬──────────────────────────┘
                              │
                              ▼
        ◇ algum trecho com similaridade ≥ SIM_MIN ? ◇
                              │
                   ┌──────────┴─────────────────────────────┐
                  não                                      sim
                   ▼                                        ▼
┌────────────────────────────────────┐  ┌──────────────────────────────────────┐
│ "Não encontrei isso no material."  │  │ 5. responder  (Ollama Cloud)         │
│                                    │  │ trechos numerados [1], [2]...        │
│ sem chamar o modelo                │  │ + pergunta  →  resposta que          │
└────────────────────────────────────┘  │ cita as fontes                       │
                                        └──────────────────────────────────────┘
```

| Passo | Função em `app/rag.py` | Onde roda | O que acontece |
|---|---|---|---|
| 1 | `embed` | Ollama local | Texto vira vetor de 768 números; textos parecidos geram vetores próximos |
| 2 | `ingerir` | pgvector | Grava `fonte`, `titulo`, `trecho` e o vetor na tabela `chunks` |
| 3 | `buscar` | pgvector | Compara o vetor da pergunta com os dos trechos (distância de cosseno) e devolve os `k` mais parecidos |
| 4 | `pontuar` e `rerank` | Ollama local | Um modelo menor relê cada trecho e dá uma nota; reordena do mais para o menos relevante (opcional) |
| 5 | `responder` | Ollama Cloud | Se nenhum trecho passa de `SIM_MIN`, recusa **sem chamar o modelo**; senão pede a resposta citando `[1]`, `[2]` |

### Experimente com curl

> [!NOTE]
> Rode dentro do container (`docker compose exec app bash`). Dele, o Ollama **local** é alcançado pelo nome `ollama` (`http://ollama:11434`) e não precisa de chave.

**1. Embedding:** transforma um texto em um vetor de 768 números. Textos de significado parecido geram vetores próximos. O `jq` resume a resposta, que seria uma lista enorme de números:

```bash
curl -s http://ollama:11434/api/embed \
  -d '{"model":"embeddinggemma:300m","input":["Quando um índice deixa o banco mais lento?"]}' \
  | jq '{dimensoes: (.embeddings[0] | length), primeiros: .embeddings[0][:4]}'
```

A resposta é `{"dimensoes": 768, "primeiros": [-0.05, -0.04, 0.03, 0.03]}`. Sem o `jq`, você vê `{"embeddings":[[...]]}`: uma lista de vetores, um por texto de `input`. Dá para mandar vários textos de uma vez.

**2. Reranker:** pergunta ao modelo se um trecho responde à pergunta. O prompt tem um formato próprio, e pedimos as probabilidades (`logprobs`) do primeiro token:

```bash
curl -s http://ollama:11434/api/generate -d '{
  "model": "dengcao/Qwen3-Reranker-0.6B:F16",
  "raw": true,
  "stream": false,
  "options": {"temperature": 0, "num_predict": 1},
  "logprobs": true,
  "top_logprobs": 3,
  "prompt": "<|im_start|>system\nJudge whether the Document meets the requirements based on the Query and the Instruct provided. Note that the answer can only be \"yes\" or \"no\".<|im_end|>\n<|im_start|>user\n<Instruct>: Given a student question, retrieve the course passages that answer it\n<Query>: Quando um índice deixa o banco mais lento?\n<Document>: Todo índice é mantido a cada escrita: INSERT, UPDATE e DELETE ficam mais lentos.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
}' | jq '{resposta: .response, top: [.logprobs[0].top_logprobs[] | {token, logprob}]}'
```

Na resposta, `"resposta": "yes"` e, em `top`, algo como `yes: -0.2`, `Yes: -1.85`, `no: -5.58`. Quanto mais perto de 0, mais provável. A nota do trecho é `P(yes) / (P(yes) + P(no))`, calculada a partir desses números. Troque o `<Document>` por um trecho sem relação (por exemplo, sobre transações) e veja o `no` subir.

### Passo a passo

1. Leia os arquivos em [corpus/](corpus/): são 5 mini-apostilas de Banco de Dados.
2. Abra [app/rag.py](app/rag.py). O `carregar_chunks` já divide as apostilas em trechos. Implemente, na ordem:
   0. Já estão prontas `texto_de_trecho` e `texto_de_pergunta` (prefixos de tarefa que o modelo de embedding espera): use-as em `ingerir` e em `responder`;
   1. `embed`: `POST /api/embed` no Ollama **local**, com `{"model": ..., "input": [textos]}`;
   2. `ingerir`: gere os embeddings e grave os trechos na tabela `chunks` do pgvector;
   3. `buscar`: o SQL `ORDER BY embedding <=> %s` (distância de cosseno) devolve os mais parecidos;
   4. `pontuar` e `rerank` (opcionais, mas os testes do reranker só passam com eles): `pontuar(resposta)` converte os `logprobs` em nota e `rerank` a usa. O modelo local `Qwen3-Reranker` dá a cada trecho uma nota de 0 a 1 (a probabilidade de ele responder "yes" à pergunta), e você reordena do maior para o menor. Os comentários do arquivo explicam o formato do prompt. Enquanto não fizer, os candidatos ficam na ordem da busca;
   5. `responder`: junte tudo, recuse quando nada for relevante e peça ao modelo da nuvem que responda **só com base nos trechos**, citando `[1]`, `[2]`, em **texto corrido, sem Markdown** e curta (no Desafio extra você liga o Markdown).
3. Na aba **Material**, clique em **Indexar material** e pergunte: *"Quando um índice pode deixar o banco mais lento?"*
4. Pergunte algo fora do material (*"Qual a capital da França?"*): o app deve dizer que não encontrou, sem chamar o modelo.
5. Veja no terminal (`docker compose logs -f app`) as notas de similaridade de cada trecho.

### Como verificar

#### 1. Pela linha de comando

```bash
docker compose exec app pytest etapas/etapa-3
```

Todos os testes devem terminar em `PASSED`. **Demora**: na primeira vez, de 1 a 3 minutos, porque o Ollama local carrega os modelos na memória (nas execuções seguintes, cerca de 1 minuto); o mesmo atraso aparece na primeira indexação ou pergunta pela tela (o botão fica em "Indexando..." / "Buscando..."). Um dos testes mede se, em pelo menos 8 de 10 perguntas, o trecho certo aparece entre os recuperados; outro confirma que uma pergunta fora do material não chama o modelo.

#### 2. Pelo `curl`

Dentro do container, chame o **seu** endpoint, primeiro para indexar e depois para perguntar:

```bash
curl -s -X POST http://localhost:8000/ingest | jq

curl -s -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"pergunta":"Quando um índice pode deixar o banco mais lento?"}' | jq
```

O `/ingest` devolve `{"trechos_indexados": 23}`. O `/ask` devolve `{"resposta": "...", "fontes": [...]}`, em que cada fonte traz `fonte`, `trecho`, `similaridade` e, se o reranker estiver ativo, `rerank`. Para ver só o essencial de cada fonte, troque o final por:

```bash
| jq '{resposta, fontes: [.fontes[] | {fonte, similaridade, rerank}]}'
```

Repita com uma pergunta fora do material (`"Qual a capital da França?"`): a resposta é "Não encontrei isso no material." e `fontes` vem vazio.

#### 3. Pela interface

1. Abra http://localhost:8000 e entre na aba **Material**.
2. Clique em **Indexar material**: deve aparecer **"23 trechos indexados."** (o número muda se você alterar o `corpus/`).
3. Pergunte: *"Quando um índice pode deixar o banco mais lento?"* A resposta deve **citar as fontes** (`[1]`, `[2]`) e, abaixo dela, devem aparecer os **trechos usados**, cada um com `corpus/03-indices.md`, a **similaridade** e a nota do **rerank** (se estiver ativo).
4. Pergunte algo fora do material: *"Qual a capital da França?"* Deve aparecer **"Não encontrei isso no material."**, sem nenhuma fonte.

![Etapa 3 na interface: indexação, resposta com fontes e pergunta fora do material](docs/img/etapa-3.gif)

### Do embed ao banco e à pergunta (exemplo guiado)

Aqui você acompanha **um dado do começo ao fim**: o texto vira vetor, o vetor é gravado no banco, e a pergunta busca de volta. Use **dois terminais**:

- **Terminal A** (dentro do container do app, para `curl` e Python): `docker compose exec app bash`
- **Terminal B** (no seu computador, fora do container, para olhar o banco): `docker compose exec pgvector psql -U postgres -d oficina`. Isso abre o `psql`; para sair, digite `\q`.

> [!NOTE]
> Os resultados abaixo são de referência. Os números de similaridade podem variar um pouco na sua máquina. O que importa é o **formato**: 768 dimensões, 23 trechos e o trecho certo no topo.

**1. Antes de gravar: o banco**

Terminal B:

```sql
SELECT count(*) FROM chunks;
```

Se você nunca indexou, o resultado é `0` (a tabela existe, criada por `db/init.sql`, mas está vazia).

**2. Embed: o texto vira vetor**

Terminal A, com um dos trechos da apostila:

```bash
curl -s http://ollama:11434/api/embed \
  -d '{"model":"embeddinggemma:300m","input":["title: O custo das escritas | text: Todo índice é mantido a cada escrita na tabela."]}' \
  | jq '{dimensoes: (.embeddings[0] | length), primeiros: .embeddings[0][:3]}'
```

Resultado: `"dimensoes": 768` e uma lista de números pequenos (positivos e negativos). Esse vetor de 768 posições é o que o `embed` devolve para cada trecho.

**3. Gravar: indexar o material**

Terminal A (ou clique em **Indexar material** na tela):

```bash
curl -s -X POST http://localhost:8000/ingest | jq
```

Resultado: `{"trechos_indexados": 23}`. É o `ingerir`: para cada trecho, ele chamou o `embed` e gravou uma linha na tabela `chunks`.

**4. Conferir o que foi salvo**

Terminal B. Primeiro, quantos trechos há por apostila:

```sql
SELECT fonte, count(*) AS trechos FROM chunks GROUP BY fonte ORDER BY fonte;
```

```text
        fonte        | trechos
---------------------+---------
 01-modelagem.md     |       4
 02-normalizacao.md  |       5
 03-indices.md       |       5
 04-transacoes.md    |       4
 05-consultas-sql.md |       5
```

A soma é 23, o mesmo número do `/ingest`. Agora, o tamanho de cada vetor gravado:

```sql
SELECT fonte, titulo, vector_dims(embedding) AS dimensoes FROM chunks ORDER BY id LIMIT 3;
```

```text
      fonte      |               titulo               | dimensoes
-----------------+------------------------------------+-----------
 01-modelagem.md | Entidades e atributos              |       768
 01-modelagem.md | Relacionamentos e cardinalidade    |       768
 01-modelagem.md | Chave primária e chave estrangeira |       768
```

Todos com `768`, o mesmo tamanho da coluna `embedding vector(768)` em `db/init.sql`. Para **ver** o vetor (só o começo, ele é longo):

```sql
SELECT titulo, left(embedding::text, 60) || '...' AS vetor FROM chunks ORDER BY id LIMIT 2;
```

Indexar de novo **não duplica**: rode o passo 3 outra vez e repita `SELECT count(*) FROM chunks;`. Deve continuar `23`, porque o `ingerir` apaga a tabela (`TRUNCATE`) antes de gravar.

**5. Perguntar: a busca vetorial no banco**

A pergunta também vira vetor (com `embed`) e o banco devolve os trechos mais próximos. Para ver **só essa busca**, sem chamar o modelo da nuvem, rode no Terminal A:

```bash
python - <<'EOF'
import asyncio
from app.rag import embed, texto_de_pergunta, buscar

[vetor] = asyncio.run(embed([texto_de_pergunta("Quando um índice pode deixar o banco mais lento?")]))
print(len(vetor), "dimensões")
for c in buscar(vetor, 4):
    print(f"{c['similaridade']:.3f}  {c['fonte']}  {c['titulo']}")
EOF
```

```text
768 dimensões
0.528  03-indices.md  O custo das escritas
0.463  03-indices.md  O que é um índice
0.449  03-indices.md  Quando um índice ajuda
0.436  03-indices.md  Baixa seletividade
```

O trecho **"O custo das escritas"** lidera, e é ele que responde à pergunta. Você também pode fazer essa busca direto no SQL, usando um trecho gravado como se fosse a pergunta (Terminal B). A primeira linha é o próprio trecho, com similaridade `1.000`:

```sql
SELECT fonte, titulo,
       round((1 - (embedding <=> (SELECT embedding FROM chunks WHERE titulo = 'O custo das escritas')))::numeric, 3) AS similaridade
FROM chunks
ORDER BY embedding <=> (SELECT embedding FROM chunks WHERE titulo = 'O custo das escritas')
LIMIT 4;
```

Por fim, pergunte de verdade (Terminal A) e compare:

```bash
curl -s -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"pergunta":"Quando um índice pode deixar o banco mais lento?"}' \
  | jq '{resposta, fontes: [.fontes[] | {fonte, similaridade, rerank}]}'
```

As `fontes` são os mesmos trechos da busca acima, com os mesmos valores de `similaridade`. A **ordem** pode mudar: o `/ask` reordena pelo `rerank`, e a busca pura ordena só pela similaridade. Assim você enxerga a cadeia completa: **texto → embed → vetor gravado → busca → rerank → resposta**.

### Se der erro

| Sintoma | O que fazer |
|---|---|
| "Não consegui falar com um dos serviços" | `docker compose ps`: veja se `ollama` e `pgvector` estão saudáveis |
| Busca devolve vazio | Clique em **Indexar material** antes de perguntar |
| "Não encontrei isso no material" para tudo | O limiar `SIM_MIN` do `.env` está alto demais; baixe e compare |
| Reranker lento ou falhando | Coloque `RERANK_ENABLED=false` no `.env`: o RAG continua funcionando só com a busca |

### Desafio extra

**Markdown na resposta.** A aba **Material** já sabe **renderizar Markdown** (negrito, listas, tabelas e blocos de código). Ajuste o prompt de `responder` para o modelo responder em Markdown (por exemplo, uma lista curta e as fontes `[1]`, `[2]` em **negrito**), pergunte de novo e veja a diferença na tela.

**Reranker.** Compare os resultados com e sem o reranker (`RERANK_ENABLED`). Em quais perguntas a ordem dos trechos muda?

**Banco.** Repita as consultas da seção "Do embed ao banco e à pergunta" depois de mudar o `corpus/` (por exemplo, acrescentando um `## Título` novo em uma apostila) e indexar de novo: o `count` muda?

---

## Etapa 4: Desafio livre (30 min)

Use o que construiu para criar algo seu. A rota `GET /extra/ping` em [app/extra.py](app/extra.py) já está incluída no app: acrescente suas rotas ali.

Sugestão: um **quiz sobre o material**. Receba um tema, recupere os trechos com `texto_de_pergunta`, `embed`, `buscar` e `rerank`, passe-os como `contexto` para `gerar_quiz` e devolva as questões. Outras ideias: resumir um arquivo do corpus, gerar flashcards, avaliar a resposta escrita de um aluno.

### Como verificar

#### 1. Pela linha de comando

```bash
docker compose exec app pytest etapas/etapa-4
```

#### 2. Pelo `curl`

Se você fizer o quiz sobre o material, chame, dentro do container, com:

```bash
curl -s -X POST http://localhost:8000/extra/quiz-material \
  -H "Content-Type: application/json" \
  -d '{"tema":"Transações","n":1}' | jq
```

#### 3. Pela interface

A tela do app não tem um botão para as suas rotas novas, mas o FastAPI gera uma página de testes para **todas** elas:

1. Abra http://localhost:8000/docs.
2. Abra a rota (por exemplo, `POST /extra/quiz-material`) e clique em **Try it out**.
3. Edite o corpo (`{"tema": "Transações", "n": 1}`) e clique em **Execute**.
4. Em **Server response**, o código deve ser **200** e o corpo, o quiz gerado. Logo acima, a página mostra o `curl` equivalente.

![Etapa 4 na interface: página /docs do FastAPI testando a rota do quiz sobre o material](docs/img/etapa-4.gif)

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
| `docker compose exec app bash` | Entrar no container: `curl`, `jq`, `pytest` e a chave (do `.env`) já estão lá. Saia com `exit` |
| `docker compose exec app pytest etapas/etapa-N -q` | Testar a etapa N sem entrar no container |

## Estrutura do projeto

```text
app/            seu código (os arquivos com "ETAPA" nos comentários são os seus exercícios)
 |-static/      Telas (HTML pronto)
corpus/         as apostilas usadas pelo RAG
etapas/         soluções de referência, testes e perguntas de verificação
scripts/        etapa.py: prepara ou aplica uma etapa
docs/           material do instrutor e do apoio (e os GIFs do README em docs/img)
docker-compose.yml, .env.example, db/init.sql
```

## Conheça mais da Tecnisys

Os produtos da **Tecnisys** abaixo **não fazem parte do exercício**: estão aqui para quem quiser conhecer onde essas ideias (dados, banco de dados e IA) aparecem em plataformas profissionais. O Estuda.AI, repare, é um projeto didático e **não é** nenhum deles.

### TDP: Tecnisys Data Platform

Distribuição **curada e com suporte** da *Modern Data Stack* open source: Spark, Iceberg, Kafka, Trino, Airflow, NiFi, Superset e outras. A TDP **não é um fork**: a Tecnisys certifica uma combinação testada de projetos Apache e open source, com segurança, governança, ferramentas de instalação e atualização e suporte em português.

- **Duas edições na versão 3.0.0:** *Datacenter* (instalação local, gerenciada pelo Apache Ambari, com HDFS/Ozone e YARN) e *Kubernetes* (nativa de nuvem, com Helm e ArgoCD).
- **Para quem:** organizações que querem infraestrutura de dados aberta, sem dependência de fornecedor, inclusive em ambientes locais e regulados, e um *lakehouse* (Iceberg ou Delta com Spark e Trino) já integrado.
- **Documentação:** https://docs.tecnisys.com.br/tdp

### PostgreSYS

Ecossistema **PostgreSQL** curado para produção, em uma distribuição única e com versões testadas em conjunto: PostgreSQL, PgBouncer (pool de conexões), pgBackRest (backup e restauração), Patroni, etcd e HAProxy (alta disponibilidade), e Prometheus, Grafana e Alertmanager (monitoramento). Tudo é instalado e operado pelo **PgSmart**, um painel de controle com **CLI e interface web**.

- **Versão consultada:** PostgreSYS 4.1 (PgSmart 4.1.1).
- **Extensões:** o PostgreSYS também provisiona **pgvector**, a mesma extensão que guarda os vetores na Etapa 3 desta oficina, e PostGIS.
- **Documentação:** https://docs.tecnisys.com.br/pgsys

### CLAIM: Corporate Layer for AI Management

Plataforma de **IA empresarial para inteligência documental**: o usuário faz perguntas em linguagem natural sobre os dados da própria organização e recebe respostas baseadas neles. Usa **RAG** com arquitetura multi-tenant, roda **on-premises**, é segura e multilíngue. É a mesma técnica da Etapa 3, em escala corporativa.

- **Site do produto:** https://claim.tecnisys.com.br/pt-br
- **Documentação:** https://claim.tecnisys.com.br/pt-br/docs (em inglês: https://claim.tecnisys.com.br/en/docs)
- **Instalação e implantação:** https://github.com/Tecnisys-OSS/claim-deploy (inclui o `claimctl` e os modelos para Helm/Kubernetes, OpenShift e Docker Compose)

> [!NOTE]
> Os resumos acima foram conferidos com a documentação pública em julho e agosto de 2026. Versões e recursos mudam: consulte sempre os links oficiais para o estado atual.

## Segurança e privacidade

- A chave de API é pessoal: não a compartilhe e não a envie ao Git.
- O que você digita no app vai para o ollama.com: **não escreva dados pessoais** durante a oficina.
- A senha do banco (`oficina`) serve só para este ambiente local. Não reutilize este arranjo em produção.

## Autor

**Flaviano O. Silva**

[![LinkedIn](https://img.shields.io/badge/LinkedIn-fosbsb-0A66C2?style=flat-square)](https://www.linkedin.com/in/fosbsb/)

Contato, dúvidas e sugestões sobre a oficina: https://www.linkedin.com/in/fosbsb/

## Aviso

- **Nome fictício.** "Estuda.AI" é um nome inventado para esta oficina. Não representa, não é afiliado e não faz referência a nenhum produto, serviço, empresa ou marca existente. O nome não passou por busca de anterioridade nem por registro de marca: se você quiser usar este projeto fora do contexto educacional, **escolha e verifique o seu próprio nome**.
- **Marcas da Tecnisys.** TDP, PostgreSYS, PgSmart e CLAIM são produtos e marcas da Tecnisys, citados apenas como contexto. O Estuda.AI não é um desses produtos.
- **Marcas de terceiros.** Ollama, Docker, PostgreSQL, pgvector, FastAPI, Python, Qwen, Gemma, gpt-oss, Nemotron e demais nomes citados pertencem aos seus respectivos titulares. Eles aparecem apenas para identificar as tecnologias usadas na oficina, **sem qualquer afiliação ou endosso**. Os logotipos dos badges são fornecidos pelo [shields.io](https://shields.io).
- **Uso educacional.** O código é um exemplo para aprender, não um produto pronto. Ele é entregue **no estado em que está, sem garantias** (veja a licença abaixo) e não deve ser usado em produção sem revisão, em especial quanto a segurança, privacidade e custos de uso das APIs.

## Licença

Distribuído sob a licença MIT. Veja [LICENSE](LICENSE).
