"""Tabelas e gráficos derivados exclusivamente dos resultados medidos."""
import csv
import html
import json
import math
from pathlib import Path


def grafico(resultados, campo, titulo, unidade):
    altura = 120 + len(resultados) * 30
    maximo = max((r[campo] for r in resultados), default=1) or 1
    # Escala linear explícita: valores pequenos continuam disponíveis na legenda.
    partes = [f'<svg xmlns="http://www.w3.org/2000/svg" width="1100" height="{altura}" viewBox="0 0 1100 {altura}">',
        '<rect width="100%" height="100%" fill="white"/>',
        '<g font-family="Arial, sans-serif" fill="#222">',
        f'<text x="25" y="30" font-size="20">{html.escape(titulo)}</text>',
        f'<text x="25" y="55" font-size="12">Escala linear · {unidade} · medidas da execução exportada</text>']
    for i, r in enumerate(resultados):
        y = 80 + i * 30
        valor = r[campo]
        partes.append(f'<text x="25" y="{y + 14}" font-size="11">{html.escape(r["cenario"])} / {html.escape(r["algoritmo"])} / n={r["n"]}</text>')
        partes.append(f'<rect x="440" y="{y}" width="{valor / maximo * 490:.3f}" height="20" fill="{"#b61d38" if r["obrigatorio"] else "#59647b"}"/>')
        partes.append(f'<text x="945" y="{y + 14}" font-size="11">{valor:.6f} {unidade}</text>')
    partes.append('</g></svg>')
    return ''.join(partes)


def salvar(dados, pasta):
    pasta = Path(pasta)
    pasta.mkdir(parents=True, exist_ok=True)
    (pasta / 'medicoes.json').write_text(json.dumps(dados, ensure_ascii=False, indent=2), encoding='utf-8')
    campos = ['cenario', 'algoritmo', 'n', 'obrigatorio', 'mediana_s', 'min_s', 'max_s',
              'pico_memoria_bytes', 'execucoes_memoria', 'validado']
    with (pasta / 'medicoes.csv').open('w', newline='', encoding='utf-8-sig') as f:
        w = csv.writer(f, delimiter=';')
        w.writerow(campos + [f'tempo_{i + 1}_s' for i in range(dados['repeticoes'])])
        for r in dados['resultados']:
            w.writerow([r[k] for k in campos] + r['tempos_s'])
    for campo, nome, titulo, unidade in [('mediana_s', 'tempos.svg', 'Tempo mediano de ordenação', 's'),
            ('pico_memoria_bytes', 'memoria.svg', 'Pico de alocações auxiliares Python (tracemalloc)', 'bytes')]:
        (pasta / nome).write_text(grafico(dados['resultados'], campo, titulo, unidade), encoding='utf-8')
    linhas = ''.join('<tr>' + ''.join(f'<td>{html.escape(str(r[k]))}</td>' for k in campos) + '</tr>' for r in dados['resultados'])
    texto = f'''<!doctype html><html lang="pt-BR"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Score Arena — dados experimentais</title><style>body{{font:15px/1.6 Arial;margin:35px;color:#222}}table{{border-collapse:collapse;font-size:12px}}td,th{{border:1px solid #ccc;padding:8px;text-align:left}}img{{width:100%;max-width:1100px}}pre{{white-space:pre-wrap}}.scroll{{overflow:auto}}</style>
<h1>Score Arena — dados experimentais</h1><p>Execução iniciada em UTC: {html.escape(dados['criado_em_utc'])}. Esta página contém medições; não é o relatório acadêmico.</p>
<h2>Ambiente e método</h2><pre>{html.escape(json.dumps({k: dados[k] for k in ('python','sistema','processador','metodo')}, ensure_ascii=False, indent=2))}</pre>
<p>O pico medido não corresponde à memória total do programa. Os tempos de memória não são incluídos na mediana.</p>
<h2>Resultados</h2><div class="scroll"><table><thead><tr>{''.join('<th>'+k+'</th>' for k in campos)}</tr></thead><tbody>{linhas}</tbody></table></div>
<h2>Tempo</h2><img src="tempos.svg" alt="Gráfico de medianas em segundos"><h2>Memória</h2><img src="memoria.svg" alt="Gráfico de pico de memória auxiliar">
<p>Tempos individuais, hashes dos arquivos e metadados completos: medicoes.json. Tabela para planilha: medicoes.csv.</p></html>'''
    (pasta / 'visualizar_resultados.html').write_text(texto, encoding='utf-8')
