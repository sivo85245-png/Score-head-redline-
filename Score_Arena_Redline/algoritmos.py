"""Ordenação crescente de registros (nome, score), com eventos para animação."""

def quick_sort(dados):
    """Quick Sort iterativo, pivô central e partição em três regiões.

    Emite (tipo, índice_a, índice_b). Não usa sort/sorted.
    Empilha a maior partição antes da menor para limitar a pilha.
    """
    pilha = [(0, len(dados) - 1)]
    while pilha:
        inicio, fim = pilha.pop()
        if inicio >= fim:
            continue
        pivo = dados[(inicio + fim) // 2][1]
        menor = atual = inicio
        maior = fim
        while atual <= maior:
            yield ('comparacao', atual, maior)
            if dados[atual][1] < pivo:
                if atual != menor:
                    dados[atual], dados[menor] = dados[menor], dados[atual]
                    yield ('troca', atual, menor)
                menor += 1
                atual += 1
            else:
                yield ('comparacao', atual, maior)
                if dados[atual][1] > pivo:
                    if atual != maior:
                        dados[atual], dados[maior] = dados[maior], dados[atual]
                        yield ('troca', atual, maior)
                    maior -= 1
                else:
                    atual += 1
        esquerda, direita = (inicio, menor - 1), (maior + 1, fim)
        if esquerda[1] - esquerda[0] > direita[1] - direita[0]:
            pilha.extend((esquerda, direita))
        else:
            pilha.extend((direita, esquerda))


def heap_sort(dados):
    """Heap Sort iterativo com heap máximo; espaço auxiliar O(1)."""
    def descer(raiz, tamanho):
        while 2 * raiz + 1 < tamanho:
            filho = 2 * raiz + 1
            if filho + 1 < tamanho:
                yield ('comparacao', filho, filho + 1)
                if dados[filho + 1][1] > dados[filho][1]:
                    filho += 1
            yield ('comparacao', raiz, filho)
            if dados[raiz][1] >= dados[filho][1]:
                break
            dados[raiz], dados[filho] = dados[filho], dados[raiz]
            yield ('troca', raiz, filho)
            raiz = filho
    for raiz in range(len(dados) // 2 - 1, -1, -1):
        yield from descer(raiz, len(dados))
    for fim in range(len(dados) - 1, 0, -1):
        dados[0], dados[fim] = dados[fim], dados[0]
        yield ('troca', 0, fim)
        yield from descer(0, fim)


ALGORITMOS = {'Quick Sort': quick_sort, 'Heap Sort': heap_sort}
