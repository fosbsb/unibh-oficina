# Modelagem de dados

Apostila de apoio da oficina. Reúne os conceitos básicos para desenhar um banco de dados relacional.

## Entidades e atributos

Uma entidade representa algo do mundo real sobre o qual queremos guardar informação, como Aluno, Disciplina ou Matrícula. Cada entidade vira uma tabela, e cada atributo vira uma coluna. Um atributo descreve uma propriedade da entidade, como o nome do aluno ou a data de nascimento. Um bom modelo começa listando as entidades antes de pensar em colunas.

## Relacionamentos e cardinalidade

Um relacionamento liga duas entidades e a cardinalidade diz quantas ocorrências de uma lado se ligam ao outro. Em um relacionamento um-para-muitos, um curso tem vários alunos, mas cada aluno pertence a um único curso. Em um relacionamento muitos-para-muitos, um aluno cursa várias disciplinas e cada disciplina tem vários alunos. Relacionamentos muitos-para-muitos não cabem diretamente em duas tabelas: é preciso criar uma tabela associativa, como Matrícula, com as chaves das duas entidades.

## Chave primária e chave estrangeira

A chave primária identifica cada linha de uma tabela de forma única e não pode ser nula. Pode ser um identificador artificial, como um número sequencial, ou uma chave natural, como o CPF. A chave estrangeira é uma coluna que aponta para a chave primária de outra tabela e garante a integridade referencial: o banco recusa uma matrícula que aponte para um aluno inexistente. Em uma tabela associativa, a chave primária costuma ser composta pelas duas chaves estrangeiras.

## Restrições de integridade

Além das chaves, o banco aceita restrições que protegem os dados: NOT NULL impede valores ausentes, UNIQUE impede repetição e CHECK valida uma regra, como exigir que a nota fique entre 0 e 10. Colocar essas regras no banco, e não só na aplicação, evita que dados inválidos entrem por qualquer caminho.
