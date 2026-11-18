"""Experimento reproduzível: tempo sem instrumentação; memória em outra execução."""
import argparse
from collections import Counter
from datetime import datetime, timezone
import gc
import hashlib
import platform
from pathlib import Path
import statistics
import sys
import time
import tracemalloc
from dados import BASE, CENARIOS, carregar, ordenado
from ordenacao import ALGORITMOS, OBRIGATORIOS

class Cancelado(Exception):
    pass

def executar(progresso=None, cancelar=None, tamanhos=(20000,), repeticoes=3, nomes=None):
    tamanhos = tuple(tamanhos)
    nomes = tuple(nomes or ALGORITMOS)
    if repeticoes not in (3, 4, 5) or not tamanhos or any(n not in (2500, 5000, 10000, 20000) for n in tamanhos):
        raise ValueError('Use 3 a 5 repetições e tamanhos 2500, 5000, 10000 ou 20000.')
    if any(nome not in ALGORITMOS for nome in nomes):
        raise ValueError('Algoritmo desconhecido.')
    total = len(CENARIOS) * len(tamanhos) * len(nomes) * (repeticoes + 1)
    concluidas = 0
    inicio_total = time.perf_counter()
    resultado = {'versao': 4, 'criado_em_utc': datetime.now(timezone.utc).isoformat(),
        'python': sys.version, 'sistema': platform.platform(), 'processador': platform.processor(),
        'maquina': platform.machine(), 'repeticoes': repeticoes, 'tamanhos': list(tamanhos),
        'algoritmos': list(nomes), 'arquivos': [], 'resultados': [],
        'metodo': {'tempo': 'perf_counter; apenas ordenação; mediana de execuções sem instrumentação',
            'memoria': 'Uma execução separada por combinação: pico de alocações Python rastreadas por tracemalloc. Exclui entrada, cópia e validação; não é RSS do processo.',
            'entrada': 'Primeiros n registros originais, cópia nova em cada execução; CSV não alterado.',
            'aquecimento': 'Uma chamada por algoritmo com 100 registros antes de medir cada cenário/tamanho.',
            'ordem': 'Ordem dos algoritmos alternada entre repetições; garbage collector mantido habilitado.',
            'validacao': 'Ordem crescente e Counter dos pares (name, score) após cada execução.',
            'quick': 'Pivô central, três regiões, pilha explícita; diferente do pivô inicial da tabela do professor.',
            'escopo': 'Quick Sort e Heap Sort, conforme orientação específica do grupo informada pelo usuário.'}}
    def anunciar(texto):
        if cancelar and cancelar.is_set():
            raise Cancelado('Cancelado ao terminar a execução anterior.')
        if progresso:
            progresso({'mensagem': texto, 'concluidas': concluidas, 'total': total})
    def validar(a, referencia):
        if not ordenado(a) or Counter(a) != referencia:
            raise AssertionError('Ordem ou integridade dos registros inválida.')
    for cenario, arquivo in CENARIOS.items():
        caminho = BASE / 'dados' / f'4_player_scores_{arquivo}.csv'
        original_completo = carregar(cenario)
        if len(original_completo) != 20000:
            raise ValueError(f'{cenario}: esperado 20.000 registros.')
        resultado['arquivos'].append({'cenario': cenario, 'arquivo': caminho.name,
            'sha256': hashlib.sha256(caminho.read_bytes()).hexdigest(), 'registros': len(original_completo)})
        for n in tamanhos:
            original = original_completo[:n]
            referencia = Counter(original)
            tempos = {nome: [] for nome in nomes}
            for nome in nomes:
                anunciar(f'{cenario} · n={n} · aquecimento · {nome}')
                ALGORITMOS[nome](original[:100])
            for repeticao in range(repeticoes):
                ordem = nomes if repeticao % 2 == 0 else nomes[::-1]
                for nome in ordem:
                    anunciar(f'{cenario} · n={n} · {nome} · tempo {repeticao + 1}/{repeticoes}')
                    copia = original.copy()
                    inicio = time.perf_counter()
                    ALGORITMOS[nome](copia)
                    tempos[nome].append(time.perf_counter() - inicio)
                    validar(copia, referencia)
                    concluidas += 1
            for nome in nomes:
                anunciar(f'{cenario} · n={n} · {nome} · memória (execução separada; pode demorar)')
                copia = original.copy()
                gc.collect()
                tracemalloc.start()
                try:
                    ALGORITMOS[nome](copia)
                    _, pico = tracemalloc.get_traced_memory()
                finally:
                    tracemalloc.stop()
                validar(copia, referencia)
                concluidas += 1
                resultado['resultados'].append({'cenario': cenario, 'algoritmo': nome, 'n': n,
                    'obrigatorio': nome in OBRIGATORIOS, 'tempos_s': tempos[nome],
                    'mediana_s': statistics.median(tempos[nome]), 'min_s': min(tempos[nome]),
                    'max_s': max(tempos[nome]), 'pico_memoria_bytes': pico,
                    'execucoes_memoria': 1, 'validado': True})
    anunciar('Concluído: todas as ordenações e registros validados.')
    resultado['duracao_total_s'] = time.perf_counter() - inicio_total
    return resultado

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--crescimento', action='store_true', help='Também mede n=2500, 5000 e 10000.')
    parser.add_argument('--repeticoes', type=int, choices=(3, 4, 5), default=3)
    parser.add_argument('--saida', default=str(BASE / 'resultados'))
    args = parser.parse_args()
    def log(p):
        print(f"[{p['concluidas']}/{p['total']}] {p['mensagem']}", flush=True)
    resultado = executar(log, tamanhos=(2500, 5000, 10000, 20000) if args.crescimento else (20000,),
        repeticoes=args.repeticoes)
    from exportar import salvar
    salvar(resultado, Path(args.saida))
    print(f'Arquivos gravados em: {Path(args.saida).resolve()}', flush=True)

if __name__ == '__main__':
    main()
