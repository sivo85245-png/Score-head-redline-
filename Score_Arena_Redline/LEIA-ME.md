# Score Arena Redline — Quick Sort e Heap Sort / versão 4

APS de ordenação de Player Scores com **Quick Sort e Heap Sort**, conforme a orientação específica do professor informada pelo grupo. O jogo, os colegas destacados, a corrida e o duelo foram mantidos.

## Abrir

1. Extrai o ZIP inteiro.
2. Abre **INICIAR.bat**, com Python 3.10 ou superior instalado.
3. No navegador, abre **Laboratório APS** e clica em **Medir em Python**.
4. Exporta JSON/CSV ou abre a pasta **resultados**, criada no projeto.

No VS Code: Arquivo → Abrir Pasta → seleciona esta pasta; no terminal, executa `python servidor.py`. Não precisas de Git nem de bibliotecas externas. Mantém o terminal aberto durante o uso.

ABRIR_JOGO.html e JOGAR_SCORE_ARENA.html funcionam sem Python para corrida, duelo e liga. As medições Python precisam de INICIAR.bat.

## O que foi melhorado

- Ordenação Python sem eventos de animação dentro do tempo medido.
- Medição de memória em execução separada, sem afetar os tempos exportados.
- Andamento, cancelamento após a execução atual e reconexão ao recarregar a página.
- Gráficos de tempo e memória, tabela e exportações CSV/JSON/SVG/HTML.
- Estudo opcional de crescimento com 2.500, 5.000, 10.000 e 20.000 registros.
- Metadados do ambiente, hashes dos CSVs e validação de ordem e integridade.

## Protocolo

O experimento padrão usa os quatro CSVs completos de 20.000 registros, os dois algoritmos e três repetições: **24 execuções de tempo + 8 de memória**.

1. Ler os CSVs, convertendo score para inteiro.
2. Aquecer cada algoritmo com os primeiros 100 registros antes de cada cenário/tamanho.
3. Copiar a entrada original antes de cada execução.
4. Medir apenas a função de ordenação com time.perf_counter. Leitura, cópia, validação, contadores e desenho ficam fora do cronômetro.
5. Alternar a ordem dos algoritmos entre repetições; conservar o coletor de lixo habilitado.
6. Guardar mediana, mínimo, máximo e todos os tempos individuais.
7. Medir memória numa execução adicional com tracemalloc, após copiar a entrada e coletar lixo. O pico corresponde a alocações auxiliares Python, não ao RSS do processo nem à memória total do computador. A lista original e sua cópia não entram no rastreamento.
8. Validar, após cada execução, ordem crescente e igualdade do multiconjunto dos pares nome/score.

Na interface, o experimento roda em processo separado do servidor HTTP, para não rastrear as alocações da interface. A comunicação de progresso é síncrona e ocorre fora das regiões medidas. Apenas uma tarefa pode rodar por vez.

Para o estudo de crescimento, marca a opção na tela ou executa:

```text
python benchmark.py --crescimento
```

São 96 execuções de tempo e 32 de memória usando os primeiros n registros de cada CSV. Para usar cinco repetições:

```text
python benchmark.py --repeticoes 5
```

Os resultados são gravados em resultados. Uma nova execução concluída sobrescreve essa pasta; copia os arquivos antes de comparar experimentos diferentes. O cancelamento não apresenta resultados parciais como completos.

## Algoritmos e complexidade

**ordenacao.py** contém os dois algoritmos oficiais usados nas medições. Nenhum usa sort/sorted.

Quick Sort: pivô central, partição em três regiões e pilha explícita, processando a menor partição primeiro. Sob permutações aleatórias de chaves distintas, tempo médio Θ(n log n); pior caso Θ(n²); espaço auxiliar O(log n). Com todas as chaves iguais, esta variante executa em Θ(n). O pivô difere do primeiro elemento usado na tabela de exemplo do PDF.

Heap Sort: heap máximo, construção O(n), ordenação com pior caso Θ(n log n), espaço auxiliar Θ(1). Sob a mesma hipótese de chaves distintas aleatórias, tempo médio Θ(n log n). Com todas as chaves iguais, as descidas param imediatamente e esta implementação pode executar em Θ(n).

Ambos ordenam registros completos por score crescente e não garantem estabilidade. O ranking inverte a exibição para mostrar o maior score primeiro; isso não altera a regra do experimento.

O, Ω e Θ são limites superior, inferior e justo, respectivamente; não são sinônimos automáticos de pior, melhor e médio caso. A análise teórica é distinta dos segundos e bytes medidos.

**algoritmos.py** conserva os geradores instrumentados da versão anterior para estudo e testes. Eles não são cronometrados no laboratório atualizado. O duelo animado usa JavaScript e não fornece tempos de execução Python.

## Jogo e dados

Corrida com doze naves: um piloto humano, onze adversários simulados e os sete colegas destacados. Setas/A/D movem a nave; espaço ativa o turbo. As pontuações da corrida são fictícias.

O duelo Quick × Heap permite pausar, avançar passo a passo e observar pivô e heap. A liga pode adicionar os doze resultados a uma cópia dos 20.000 registros. Esses 20.012 registros nunca entram nas medições oficiais. Os CSVs originais ficam intactos; os nomes variados são apenas nomes de exibição.

## Exportações para o relatório

- medicoes.json: resultados, tempos individuais, Python, sistema, processador quando disponível, data UTC e SHA-256 dos arquivos.
- medicoes.csv: tabela para planilhas, com separador ponto e vírgula e ponto decimal.
- tempos.svg e memoria.svg: gráficos vetoriais com escala linear e valores numéricos.
- visualizar_resultados.html: consulta das tabelas e dos gráficos, sem servidor.

A pasta **resultados_validacao**, quando incluída, contém medições de verificação do desenvolvimento. Para o relatório, o grupo deve realizar e guardar suas próprias medições, anotar hardware/RAM e fechar programas pesados. PREPARAR_RELATORIO.md organiza essa etapa. Relatório e slides ainda não foram produzidos.

## Testes

```text
python -m unittest testes testes_redline testes_requisitos -v
python validar_csvs.py
```

Opcional com Node:

```text
node testes_frontend.cjs
```

Os testes verificam correção, preservação de registros, medição, exportação, rotas, concorrência, cancelamento e a lógica da interface. O DOM simulado não substitui uma inspeção visual real no navegador.

## Autoria e escopo

O usuário confirmou que o professor orientou seu grupo a trabalhar somente com Quick Sort e Heap Sort. Essa definição específica foi aplicada, embora o PDF geral apresente outra lista.

O projeto foi produzido com auxílio de IA, conforme solicitado. O PDF restringe esse uso; essa condição precisa ser tratada com o professor e declarada fielmente. Não há garantia de nota ou alegação de autoria exclusivamente humana.
