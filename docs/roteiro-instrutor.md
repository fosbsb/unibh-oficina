# Roteiro do instrutor (~4h)

Formato: explicação curta de cada etapa (5 a 10 min), depois os alunos fazem sozinhos com o README, e o apoio circula. Ao fim de cada etapa, uma demonstração de 5 min com a solução.

Mensagem central, repetida em todas as etapas: **o LLM é um componente do sistema, não só uma ferramenta para escrever código.**

## Visão geral dos tempos

| Bloco | Tempo | Marco de sucesso |
|---|---|---|
| Abertura | 10 min | Alunos entendem o objetivo e o mapa das etapas |
| Etapa 0, setup | 30 min | Selo verde e `pytest etapas/etapa-0` passando |
| Etapa 1, tutor | 50 min | Resposta em streaming na aba Tutor |
| Pausa | 10 min | |
| Etapa 2, quiz | 60 min | Quiz gerado e validado |
| Etapa 3, RAG | 70 min | Resposta citando a fonte e recusa fora do material |
| Etapa 4, livre | 30 min | Cada um mostra algo seu |
| Encerramento | 10 min | Retrospectiva e próximos passos |

Os tempos somam ~4h40 com abertura, pausa e encerramento. Se o tempo apertar, a etapa 4 é a primeira a ser cortada, e o reranker (etapa 3) pode ser mostrado em vez de feito.

## Abertura (10 min)

- Pergunta para a turma: "Onde vocês já usam IA?" Quase todos responderão "para gerar código".
- Contraste: hoje a IA roda **dentro do app**, chamada por código, com entrada e saída que o programa controla.
- Mostrar o diagrama do README: navegador, app, Ollama Cloud, Ollama local, pgvector.

## Etapa 0: Setup (30 min)

- **Ponto de parada:** todos com o selo verde antes de seguir. Quem travar usa o apoio.
- **Explicação (5 min):** um LLM é um serviço HTTP. Mostrar o corpo de `/api/chat` na tela. A chave é pessoal.
- **Pergunta para a turma:** "O que acontece se eu commitar o `.env`?"
- **Demonstração:** `chat_once` funcionando e o teste passando.

## Etapa 1: Tutor (50 min)

- **Explicação (5 min):** `messages` com papéis (`system`, `user`, `assistant`); o system prompt define comportamento; streaming em NDJSON.
- **Experimento guiado:** mudar o system prompt (por exemplo, "responda como um pirata") e ver o comportamento mudar sem tocar no código.
- **Pergunta para a turma:** "Quando um `if/else` seria melhor que o LLM?"
- **Atenção:** `gpt-oss` "pensa" antes de responder, então há alguns segundos sem texto. Avisar para ninguém achar que travou.

## Etapa 2: Quiz (60 min)

- **Explicação (10 min):** o app precisa de dados, não de texto. Mostrar o `Quiz` do Pydantic e o `quiz_exemplo.json`.
- **Ponto de parada:** conversar sobre o retry. Provocar: "e se o modelo errar três vezes?" (o app devolve erro claro, e não dado quebrado).
- **Pergunta para a turma:** "Por que validar se o modelo é inteligente?"

## Etapa 3: RAG (70 min)

- **Explicação (10 min):** mostrar uma pergunta sobre a apostila **sem** RAG (o modelo inventa) e **com** RAG (cita a fonte). Desenhar: texto, vetor, busca por similaridade, prompt.
- **Gancho do tema:** estamos em uma aula de Banco de Dados e a busca é uma consulta SQL com `<=>`. Rodar `psql` e olhar a tabela `chunks`.
- **Ponto de parada:** primeiro `embed` e `ingerir`; só depois `buscar`; só depois `responder`. O reranker é opcional.
- **Pergunta para a turma:** "Por que não mandar o corpus inteiro no prompt?" (custo, limite de contexto, ruído).
- **Demonstração:** perguntar algo fora do material; o app recusa sem chamar o modelo da nuvem.

## Etapa 4: Livre (30 min)

- Sugestão principal: quiz sobre o material (`/extra/quiz-material`).
- Cada aluno ou dupla mostra em 1 minuto o que fez.

## Encerramento (10 min)

- O que cada capacidade ensinou: prompt, saída validada, grounding.
- Próximos passos: tool calling (o modelo chama funções do seu app), avaliação automática, deploy.
- Lembrar: as chaves são pessoais; revogar se compartilharam por engano.

## Para o apoio

- Ler [docs/erros-comuns.md](erros-comuns.md) antes.
- Regra de ouro: olhar o selo da página e `docker compose ps` antes de mexer no código.
- Se o aluno estiver mais de uma etapa atrasado: `python scripts/etapa.py solucao N`.
