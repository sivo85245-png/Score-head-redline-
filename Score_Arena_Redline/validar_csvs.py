"""Validação completa de correção; não substitui o experimento de desempenho."""
from collections import Counter
import json
from pathlib import Path
from dados import carregar, CENARIOS, ordenado
from ordenacao import ALGORITMOS

def main():
    resultados = []
    for cenario in CENARIOS:
        original = carregar(cenario)
        assert len(original) == 20000
        referencia = Counter(original)
        for nome, algoritmo in ALGORITMOS.items():
            a = original.copy()
            algoritmo(a)
            assert ordenado(a) and Counter(a) == referencia, (cenario, nome)
            item = {'cenario': cenario, 'algoritmo': nome, 'n': len(a), 'ordem_e_integridade': True}
            resultados.append(item)
            print(f'OK {len(resultados)}/8: {cenario} / {nome} / 20.000 registros', flush=True)
    caminho = Path(__file__).resolve().parent / 'VALIDACAO_CSVS.json'
    caminho.write_text(json.dumps({'tipo': 'Teste de correção, não benchmark', 'resultados': resultados}, ensure_ascii=False, indent=2), encoding='utf-8')

if __name__ == '__main__':
    main()
