import ast
from collections import Counter
import random
import tempfile
import unittest
from unittest.mock import patch
from pathlib import Path
from ordenacao import ALGORITMOS, OBRIGATORIOS
from dados import ordenado
from benchmark import executar, Cancelado
from exportar import salvar
import threading

class TestRequisitos(unittest.TestCase):
    def test_todos_algoritmos(self):
        rng = random.Random(77)
        valores = [[], [4], [3, 1], [-5, 0, -5, 8], [2]*200, list(range(200)), list(range(200, -1, -1))]
        valores += [[rng.randrange(-20, 20) for _ in range(n)] for n in (3, 17, 127, 500)]
        for nome, algoritmo in ALGORITMOS.items():
            for entrada in valores:
                with self.subTest(nome=nome, n=len(entrada)):
                    original = [(str(i), score) for i, score in enumerate(entrada)]
                    a = original.copy()
                    algoritmo(a)
                    self.assertTrue(ordenado(a))
                    self.assertEqual(Counter(a), Counter(original))

    def test_nao_usa_ordenacao_pronta(self):
        arvore = ast.parse((Path(__file__).parent / 'ordenacao.py').read_text(encoding='utf-8'))
        for node in ast.walk(arvore):
            if isinstance(node, ast.Call):
                self.assertFalse(isinstance(node.func, ast.Name) and node.func.id == 'sorted')
                self.assertFalse(isinstance(node.func, ast.Attribute) and node.func.attr == 'sort')
        self.assertEqual(set(OBRIGATORIOS), {'Quick Sort', 'Heap Sort'})

    def test_benchmark_e_exportacao(self):
        # Entradas completas ordenadas permitem verificar o protocolo rapidamente.
        original = [(str(i), i) for i in range(20000)]
        atualizacoes = []
        with patch('benchmark.carregar', return_value=original):
            data = executar(atualizacoes.append, tamanhos=(2500,), nomes=('Quick Sort', 'Heap Sort'))
        self.assertEqual(len(data['resultados']), 8)
        self.assertEqual(atualizacoes[-1]['concluidas'], atualizacoes[-1]['total'])
        for r in data['resultados']:
            self.assertEqual(len(r['tempos_s']), 3)
            self.assertTrue(r['validado'])
            self.assertGreater(r['pico_memoria_bytes'], 0)
        with tempfile.TemporaryDirectory(dir=Path(__file__).resolve().parent) as d:
            salvar(data, d)
            self.assertEqual(len(list(Path(d).iterdir())), 5)
            self.assertIn('tracemalloc', (Path(d)/'visualizar_resultados.html').read_text(encoding='utf-8'))

    def test_cancelar(self):
        evento = threading.Event()
        evento.set()
        with self.assertRaises(Cancelado):
            executar(cancelar=evento)

if __name__ == '__main__':
    unittest.main(verbosity=2)
