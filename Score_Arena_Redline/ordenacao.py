"""Ordenação crescente de registros (nome, score), sem eventos ou contadores."""

def quick_sort(a):
    # Pivô central, partição em três regiões e pilha explícita.
    pilha = [(0, len(a) - 1)]
    while pilha:
        inicio, fim = pilha.pop()
        if inicio >= fim:
            continue
        pivo = a[(inicio + fim) // 2][1]
        menor = atual = inicio
        maior = fim
        while atual <= maior:
            if a[atual][1] < pivo:
                if atual != menor:
                    a[atual], a[menor] = a[menor], a[atual]
                menor += 1
                atual += 1
            elif a[atual][1] > pivo:
                if atual != maior:
                    a[atual], a[maior] = a[maior], a[atual]
                maior -= 1
            else:
                atual += 1
        esquerda, direita = (inicio, menor - 1), (maior + 1, fim)
        # A maior entra primeiro; a menor é processada primeiro (LIFO).
        if esquerda[1] - esquerda[0] > direita[1] - direita[0]:
            pilha.extend((esquerda, direita))
        else:
            pilha.extend((direita, esquerda))

def heap_sort(a):
    def descer(raiz, tamanho):
        while 2 * raiz + 1 < tamanho:
            filho = 2 * raiz + 1
            if filho + 1 < tamanho and a[filho + 1][1] > a[filho][1]:
                filho += 1
            if a[raiz][1] >= a[filho][1]:
                break
            a[raiz], a[filho] = a[filho], a[raiz]
            raiz = filho
    for raiz in range(len(a) // 2 - 1, -1, -1):
        descer(raiz, len(a))
    for fim in range(len(a) - 1, 0, -1):
        a[0], a[fim] = a[fim], a[0]
        descer(0, fim)

OBRIGATORIOS = ('Quick Sort', 'Heap Sort')
ALGORITMOS = {'Quick Sort': quick_sort, 'Heap Sort': heap_sort}
