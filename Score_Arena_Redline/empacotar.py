"""Atualiza os HTMLs independentes e cria ZIP sem caches ou resultados pessoais."""
from pathlib import Path
import zipfile

BASE = Path(__file__).resolve().parent

def main():
    pagina = (BASE/'web/index.html').read_text(encoding='utf-8')
    pagina = pagina.replace('<link rel="stylesheet" href="style.css">', '<style>' + (BASE/'web/style.css').read_text(encoding='utf-8') + '</style>')
    for nome in ('datasets.js', 'engine.js', 'render.js', 'app.js'):
        codigo = (BASE/'web'/nome).read_text(encoding='utf-8').replace('</script', '<\\/script')
        pagina = pagina.replace(f'<script src="{nome}"></script>', '<script>' + codigo + '</script>')
    (BASE/'ABRIR_JOGO.html').write_text(pagina, encoding='utf-8')
    (BASE.parent/'JOGAR_SCORE_ARENA.html').write_text(pagina, encoding='utf-8')
    destino = BASE.parent/'Score_Arena_Quick_Heap_Atualizado.zip'
    with zipfile.ZipFile(destino, 'w', zipfile.ZIP_DEFLATED) as z:
        for p in BASE.rglob('*'):
            if p.is_file() and not any(parte in ('__pycache__', 'resultados') for parte in p.relative_to(BASE).parts) and p.suffix != '.pyc':
                z.write(p, Path(BASE.name)/p.relative_to(BASE))
    with zipfile.ZipFile(destino) as z:
        assert z.testzip() is None
    print(destino)

if __name__ == '__main__':
    main()
