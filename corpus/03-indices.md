# Índices

Apostila de apoio da oficina. Mostra como os índices aceleram consultas e quais custos eles trazem.

## O que é um índice

Um índice é uma estrutura auxiliar, normalmente uma árvore B, que permite ao banco localizar linhas sem varrer a tabela inteira. Funciona como o índice remissivo de um livro: em vez de ler todas as páginas, o banco vai direto à posição dos valores procurados. A chave primária já cria um índice automaticamente.

## Quando um índice ajuda

Um índice acelera filtros com WHERE, junções com JOIN e ordenações com ORDER BY em colunas muito consultadas. Ele rende mais em colunas de alta seletividade, isto é, com muitos valores distintos, como e-mail ou CPF. Um filtro que devolve uma pequena fração das linhas aproveita bem o índice.

## O custo das escritas

Todo índice é mantido a cada escrita na tabela. Cada INSERT, UPDATE ou DELETE também precisa atualizar os índices envolvidos, por isso o custo das escritas cresce com o número de índices. Em uma tabela com muita escrita e poucas consultas, índices demais deixam o banco mais lento do que ajudam. Os índices também ocupam espaço em disco.

## Baixa seletividade

Colunas com poucos valores distintos, como sexo ou status com três opções, raramente se beneficiam de índice. Quando o filtro devolve boa parte da tabela, o otimizador prefere varrer a tabela inteira, porque saltar entre o índice e as linhas sai mais caro do que ler tudo em sequência. Medir a seletividade antes de criar o índice evita desperdício.

## Índices compostos e EXPLAIN

Um índice composto cobre mais de uma coluna e vale pela ordem delas: um índice em (cidade, nome) ajuda filtros por cidade, ou por cidade e nome, mas não filtros só por nome. Para saber se um índice está sendo usado, o comando EXPLAIN mostra o plano de execução, indicando se o banco fez varredura sequencial ou usou o índice.
