# Normalização

Apostila de apoio da oficina. Explica como organizar tabelas para reduzir redundância e evitar anomalias.

## Por que normalizar

Tabelas com dados repetidos geram anomalias. Na anomalia de atualização, o nome de um produto aparece em muitas linhas e uma alteração esquecida deixa o dado inconsistente. Na anomalia de inserção, não é possível cadastrar um produto sem um pedido. Na anomalia de remoção, apagar o último pedido de um produto faz o próprio produto desaparecer. A normalização separa os dados em tabelas menores para evitar esses problemas.

## Primeira forma normal (1FN)

Uma tabela está na 1FN quando todos os atributos são atômicos, ou seja, cada célula guarda um único valor. Uma coluna telefones com o conteúdo "3333-1111, 3333-2222" viola a 1FN. A solução é criar uma tabela própria de telefones, com uma linha por número, ligada à pessoa por chave estrangeira.

## Segunda forma normal (2FN)

Uma tabela está na 2FN quando está na 1FN e não tem dependência parcial: todo atributo que não é chave depende da chave inteira, e não de apenas uma parte dela. Isso só importa para chaves compostas. Se a chave de itens de pedido é (pedido_id, produto_id), o nome do produto depende apenas do produto, então deve ir para a tabela de produtos.

## Terceira forma normal (3FN)

Uma tabela está na 3FN quando está na 2FN e não tem dependência transitiva: um atributo comum não pode depender de outro atributo comum. Se a tabela de clientes tem cidade e estado, e a cidade determina o estado, o estado depende da chave apenas por meio da cidade. A solução é criar uma tabela de cidades com o estado e referenciá-la pela chave estrangeira.

## Quando desnormalizar

Normalizar demais exige muitos JOINs nas consultas. Em relatórios e painéis com muita leitura, às vezes se duplica um dado de propósito para ganhar velocidade. Essa desnormalização é uma decisão consciente, que troca o risco de inconsistência por desempenho, e deve ser documentada.
