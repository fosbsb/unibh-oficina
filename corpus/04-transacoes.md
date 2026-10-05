# Transações

Apostila de apoio da oficina. Apresenta o que são transações e como o banco garante consistência com acessos simultâneos.

## O que é uma transação

Uma transação é um conjunto de operações tratado como uma unidade: ou todas acontecem, ou nenhuma. O exemplo clássico é a transferência bancária, que debita uma conta e credita outra. Se o sistema falhar entre os dois passos, o dinheiro não pode desaparecer. Uma transação começa com BEGIN e termina com COMMIT, que confirma as mudanças, ou ROLLBACK, que as desfaz.

## Propriedades ACID

As transações seguem quatro propriedades. Atomicidade: tudo ou nada. Consistência: a transação leva o banco de um estado válido a outro, respeitando as restrições. Isolamento: transações simultâneas não enxergam o trabalho pela metade uma da outra. Durabilidade: depois do COMMIT, os dados sobrevivem a uma queda do sistema.

## Níveis de isolamento

Quanto maior o isolamento, menos anomalias e menor a concorrência. No nível READ COMMITTED, uma consulta só vê dados já confirmados. No REPEATABLE READ, repetir a mesma leitura dentro da transação devolve o mesmo resultado. No SERIALIZABLE, o resultado é equivalente a executar as transações uma de cada vez. As anomalias típicas são a leitura suja, a leitura não repetível e a leitura fantasma.

## Bloqueios e deadlock

Para garantir o isolamento, o banco usa bloqueios. Quando uma transação altera uma linha, as outras que precisam da mesma linha esperam o término. Um deadlock acontece quando duas transações esperam uma pela outra: a primeira trava a linha A e pede a B, enquanto a segunda trava B e pede A. O banco detecta o ciclo e cancela uma das transações. Acessar as linhas sempre na mesma ordem reduz o risco.
