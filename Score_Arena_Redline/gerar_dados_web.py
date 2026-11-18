"""Gera uma cópia estática dos CSVs para o modo sem instalação, sem alterar fontes."""
import itertools
import json
import random
from pathlib import Path
from dados import carregar, CENARIOS


def generate():
    first = 'Ana Beatriz Camila Daniela Elisa Fernanda Gabriela Helena Isabela Júlia Larissa Luana Mariana Natália Olivia Patrícia Rafaela Sofia Talita Valentina André Bernardo Caio Daniel Eduardo Felipe Gustavo Henrique Igor Joaquim Leonardo Lucas Marcelo Nicolas Otávio Paulo Rafael Rodrigo Thiago Vinícius'.split()
    middle = 'Almeida Azevedo Barros Batista Campos Cardoso Carvalho Castro Correia Costa Dias Duarte Fernandes Ferreira Freitas Gomes Lima Lopes Martins Mendes Monteiro Moraes Nogueira Oliveira Pereira'.split()
    last = 'Ramos Reis Ribeiro Rocha Rodrigues Santos Silva Soares Souza Teixeira Torres Vieira Xavier Moreira Farias Cunha Melo Moura Neves Tavares'.split()
    names = [' '.join(p) for p in itertools.product(first, middle, last)]
    random.Random(2026).shuffle(names)
    data = {'names': names[:20000], 'scenarios': {}}
    for label, key in CENARIOS.items():
        data['scenarios'][key] = [[int(name.split('_')[1]), score] for name, score in carregar(label)]
    path = Path(__file__).resolve().parent / 'web' / 'datasets.js'
    path.write_text('window.APS_DATA=' + json.dumps(data, ensure_ascii=False, separators=(',', ':')) + ';\n', encoding='utf-8')
    return data


if __name__ == '__main__':
    data = generate()
    print(f"Dados gerados: {len(data['names'])} nomes, {len(data['scenarios'])} cenarios.")
