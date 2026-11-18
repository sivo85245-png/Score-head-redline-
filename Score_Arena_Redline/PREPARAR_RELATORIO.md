# Preparação do relatório — Quick Sort e Heap Sort

Escopo confirmado pelo usuário: o professor pediu Quick Sort e Heap Sort para este grupo. O roteiro abaixo organiza as evidências; não substitui o relatório ou as conclusões dos integrantes.

## Identificação a reunir

Instituição, curso, disciplina, professor, cidade, ano, integrantes reais e matrículas. Os pilotos do jogo não comprovam participação no trabalho. Confirmar o modelo de formatação adotado pelo professor e registrar com fidelidade o auxílio de IA.

## Estrutura

1. Capa e sumário.
2. Introdução: objetivo da comparação e contexto Player Scores.
3. Fundamentos de Quick Sort e Heap Sort: funcionamento, variantes, tempo, memória e estabilidade.
4. Solução desenvolvida: CSV, registros, Python, laboratório, jogo e duelo.
5. Metodologia: máquina, Python, entradas, aquecimento, cópias, repetições, mediana, memória e validação.
6. Resultados: tabelas e gráficos dos dois algoritmos nos quatro cenários; interpretação do grupo.
7. Conclusão: algoritmo adequado para cada condição e justificativa baseada nos dados.
8. Referências consultadas e verificadas pelo grupo.
9. Código-fonte conforme as orientações de entrega.

A formatação ABNT será tratada ao montar o documento; este Markdown é apenas um roteiro.

## Evidências

- dados/: os quatro CSVs originais com 20.000 registros cada.
- dados.py: leitura dos pares nome/score, com score inteiro.
- ordenacao.py: Quick Sort e Heap Sort usados no experimento.
- benchmark.py: tempo, memória, validação e metadados.
- exportar.py: tabelas e gráficos derivados dos resultados.
- resultados/: experimento executado pelo grupo.
- VALIDACAO_CSVS.json: resultado do teste de correção, não benchmark.

## Perguntas para a análise do grupo

- Qual algoritmo foi mais rápido em cada cenário? A diferença se repete entre execuções?
- Qual usou menos memória auxiliar? Como isso se relaciona à pilha do Quick e ao heap armazenado no próprio vetor?
- Como as três regiões do Quick tratam pontuações repetidas?
- Por que nosso pivô central não deve ser comparado diretamente com os tempos do pivô inicial apresentados no PDF?
- Por que os nomes precisam acompanhar os scores durante as trocas?
- O que acontece com a ordem dos jogadores que têm a mesma pontuação?
- Por que o tempo da animação não mede a eficiência do algoritmo Python?
- Como o crescimento de n afeta os tempos? Uma amostra de resultados prova uma classe assintótica?

## Cuidados de interpretação

O é limite superior, Ω é inferior e Θ é limite justo. Essas notações não significam automaticamente pior, melhor e médio caso. O caso médio da tabela teórica pressupõe permutações aleatórias de chaves distintas.

O Quick usa pivô central, três regiões e pilha explícita com menor partição processada primeiro. Seu espaço auxiliar é O(log n), tempo médio Θ(n log n) sob a hipótese acima e pior caso Θ(n²). Com todas as chaves iguais, esta variante é Θ(n).

O Heap usa espaço auxiliar Θ(1), pior caso Θ(n log n) e tempo médio Θ(n log n) sob a mesma hipótese. Com chaves todas iguais, as descidas encerram cedo e esta implementação pode executar em Θ(n).

O pico de tracemalloc mede alocações adicionais Python. Não é a memória total da aplicação nem uma prova de complexidade. Entrada, cópia, interface e validação são excluídas desse rastreamento.

## Antes de fechar

- Executar os dois algoritmos nos quatro CSVs e guardar resultados: oito combinações, três tempos e uma execução de memória por combinação.
- Anotar hardware, RAM, versão do Python e condições de execução.
- Não copiar os tempos do PDF como resultados próprios.
- Manter a corrida de 20.012 participantes somente como demonstração; o experimento usa os 20.000 originais.
- Explicar as conclusões com os próprios argumentos, apoiados nas medições.
- Declarar o auxílio real de IA e tratar sua aceitação com o professor.
