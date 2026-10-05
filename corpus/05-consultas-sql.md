# Consultas SQL

Apostila de apoio da oficina. Revisa os principais recursos da linguagem SQL para consultar dados.

## SELECT, WHERE e ORDER BY

O comando SELECT escolhe as colunas, FROM indica a tabela e WHERE filtra as linhas. ORDER BY ordena o resultado, de forma crescente por padrão, e LIMIT restringe a quantidade de linhas devolvidas. Um exemplo é SELECT nome FROM alunos WHERE curso = 'Sistemas' ORDER BY nome LIMIT 10.

## JOIN

O JOIN combina linhas de tabelas relacionadas. O INNER JOIN devolve apenas as linhas com correspondência nas duas tabelas. O LEFT JOIN devolve todas as linhas da tabela da esquerda e preenche com NULL quando não há correspondência, útil para achar alunos sem matrícula. A condição do JOIN costuma comparar a chave estrangeira com a chave primária, usando a cláusula ON.

## GROUP BY e funções de agregação

GROUP BY agrupa as linhas por uma ou mais colunas para aplicar funções de agregação como COUNT, SUM, AVG, MIN e MAX. Para contar alunos por curso, usa-se SELECT curso, COUNT(*) FROM alunos GROUP BY curso. O HAVING filtra os grupos depois da agregação, enquanto o WHERE filtra as linhas antes dela.

## Subconsultas

Uma subconsulta é um SELECT dentro de outro. Ela pode aparecer no WHERE, para filtrar por um resultado calculado, como alunos com nota acima da média da turma, ou no FROM, como uma tabela temporária. Quando a mesma subconsulta é reutilizada, uma expressão WITH (CTE) deixa o código mais legível.

## NULL

NULL representa um valor ausente ou desconhecido, e não é igual a zero nem a texto vazio. Comparações com NULL usando = nunca são verdadeiras, então o teste correto é IS NULL ou IS NOT NULL. Funções de agregação como AVG ignoram os valores NULL.
