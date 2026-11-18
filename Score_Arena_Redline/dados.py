import csv
from pathlib import Path

BASE = Path(__file__).resolve().parent
CENARIOS = {
    'Aleatório': 'aleatoria',
    'Quase ordenado': 'quase_ordenada',
    'Ordem inversa': 'ordem_inversa',
    'Muitas repetições': 'muitas_repeticoes',
}


def carregar(cenario):
    caminho = BASE / 'dados' / f'4_player_scores_{CENARIOS[cenario]}.csv'
    with caminho.open(encoding='utf-8-sig', newline='') as arquivo:
        leitor = csv.DictReader(arquivo)
        if leitor.fieldnames != ['name', 'score']:
            raise ValueError('O CSV deve ter as colunas name,score.')
        return [(linha['name'], int(linha['score'])) for linha in leitor]


def ordenado(dados):
    return all(dados[i - 1][1] <= dados[i][1] for i in range(1, len(dados)))
