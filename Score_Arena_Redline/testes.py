import random
import unittest
from collections import Counter
from algoritmos import ALGORITMOS
from dados import CENARIOS, carregar, ordenado


class TestOrdenacao(unittest.TestCase):
    def conferir(self, registros):
        for nome, algoritmo in ALGORITMOS.items():
            with self.subTest(algoritmo=nome, n=len(registros)):
                copia = registros.copy()
                for _ in algoritmo(copia):
                    pass
                self.assertTrue(ordenado(copia))
                self.assertEqual(Counter(copia), Counter(registros))
                self.assertEqual([r[1] for r in copia], sorted(r[1] for r in registros))

    def test_limites(self):
        for valores in ([], [5], [2, 1], [1, 2], [7] * 300,
                        list(range(500)), list(range(500, -1, -1)),
                        [0, -3, 8, -3, 1, 0]):
            self.conferir([(f'Player_{i}', v) for i, v in enumerate(valores)])

    def test_aleatorios(self):
        rng = random.Random(42)
        for tamanho in (3, 17, 100, 1000):
            self.conferir([(str(i), rng.randrange(30)) for i in range(tamanho)])

    def test_quatro_csv_completos(self):
        for cenario in CENARIOS:
            dados = carregar(cenario)
            self.assertEqual(len(dados), 20000)
            self.conferir(dados)


if __name__ == '__main__':
    unittest.main(verbosity=2)
