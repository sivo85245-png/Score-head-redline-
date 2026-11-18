"""Servidor local do jogo e laboratório Python com execução em segundo plano."""
import argparse
import json
import platform
import multiprocessing
import threading
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse, parse_qs
from benchmark import executar, Cancelado
from exportar import salvar

BASE = Path(__file__).resolve().parent
WEB = BASE / 'web'

def processo_medicao(fila, cancelar, crescimento):
    """Processo separado: requisições HTTP não contaminam o tracemalloc."""
    def atualizar(p):
        fila.send({'estado': 'executando', 'progresso': p})
    try:
        dados = executar(atualizar, cancelar,
            tamanhos=(2500, 5000, 10000, 20000) if crescimento else (20000,))
        salvar(dados, BASE / 'resultados')
        fila.send({'estado': 'concluido', 'dados': dados})
    except Cancelado as erro:
        fila.send({'estado': 'cancelado', 'mensagem': str(erro)})
    except Exception as erro:
        fila.send({'estado': 'erro', 'mensagem': str(erro)})

def executar_trabalho(server, crescimento):
    contexto = multiprocessing.get_context('spawn')
    receptor, emissor = contexto.Pipe(duplex=False)
    processo = contexto.Process(target=processo_medicao, args=(emissor, server.cancel_event, crescimento), daemon=True)
    try:
        processo.start()
        emissor.close()
        while True:
            if receptor.poll(1):
                estado = receptor.recv()
                server.job_state = estado
                if estado['estado'] != 'executando':
                    break
            else:
                if not processo.is_alive():
                    server.job_state = {'estado': 'erro', 'mensagem': 'O processo de medição encerrou sem concluir.'}
                    break
        processo.join(timeout=3)
    except Exception as erro:
        server.job_state = {'estado': 'erro', 'mensagem': str(erro)}
    finally:
        receptor.close()
        emissor.close()
        server.measure_lock.release()

class Handler(BaseHTTPRequestHandler):
    def log_message(self, *args):
        pass
    def send(self, data, status=200, content_type='application/json; charset=utf-8'):
        body = json.dumps(data, ensure_ascii=False).encode('utf-8') if isinstance(data, dict) else data
        self.send_response(status)
        self.send_header('Content-Type', content_type)
        self.send_header('Content-Length', str(len(body)))
        self.send_header('X-Content-Type-Options', 'nosniff')
        self.send_header('Cache-Control', 'no-store')
        self.end_headers()
        self.wfile.write(body)
    def do_GET(self):
        path = urlparse(self.path).path
        if path == '/api/health':
            return self.send({'app': 'Score Arena Redline', 'versao': 4, 'python': platform.python_version()})
        if path == '/api/benchmark':
            return self.send(self.server.job_state)
        allowed = {'/': 'index.html', '/index.html': 'index.html', '/style.css': 'style.css',
                   '/datasets.js': 'datasets.js', '/engine.js': 'engine.js',
                   '/render.js': 'render.js', '/app.js': 'app.js'}
        exports = {'/resultados/' + name: name for name in ('medicoes.json', 'medicoes.csv', 'tempos.svg', 'memoria.svg', 'visualizar_resultados.html')}
        if path in allowed:
            file = WEB / allowed[path]
        elif path in exports:
            file = BASE / 'resultados' / exports[path]
        else:
            return self.send({'erro': 'Arquivo não encontrado.'}, 404)
        mime = {'html': 'text/html', 'css': 'text/css', 'js': 'text/javascript',
                'json': 'application/json', 'csv': 'text/csv', 'svg': 'image/svg+xml'}
        try:
            self.send(file.read_bytes(), content_type=mime[file.suffix[1:]] + '; charset=utf-8')
        except OSError:
            self.send({'erro': 'Arquivo ausente. Execute a medição ou extraia o ZIP completo.'}, 404)
    def do_POST(self):
        parsed = urlparse(self.path)
        if parsed.path not in ('/api/benchmark', '/api/cancelar'):
            return self.send({'erro': 'Rota não encontrada.'}, 404)
        origin = self.headers.get('Origin')
        if origin and origin != 'http://' + self.headers.get('Host', ''):
            return self.send({'erro': 'Origem não autorizada.'}, 403)
        if parsed.path == '/api/cancelar':
            self.server.cancel_event.set()
            return self.send({'mensagem': 'Cancelamento solicitado; aguarde a execução atual terminar.'})
        if not self.server.measure_lock.acquire(blocking=False):
            return self.send({'erro': 'Uma medição já está em andamento.'}, 409)
        self.server.cancel_event.clear()
        self.server.job_state = {'estado': 'executando', 'progresso': {'mensagem': 'Preparando os arquivos…', 'concluidas': 0, 'total': 32}}
        crescimento = parse_qs(parsed.query).get('crescimento') == ['1']
        try:
            threading.Thread(target=executar_trabalho, args=(self.server, crescimento), daemon=True).start()
        except Exception:
            self.server.measure_lock.release()
            self.server.job_state = {'estado': 'erro', 'mensagem': 'Não foi possível iniciar a tarefa.'}
            raise
        return self.send({'estado': 'executando'}, 202)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', type=int, default=8765)
    parser.add_argument('--no-browser', action='store_true')
    args = parser.parse_args()
    try:
        server = ThreadingHTTPServer(('127.0.0.1', args.port), Handler)
    except OSError:
        server = ThreadingHTTPServer(('127.0.0.1', 0), Handler)
    server.measure_lock = threading.Lock()
    server.cancel_event = multiprocessing.get_context('spawn').Event()
    server.job_state = {'estado': 'pronto'}
    url = f'http://127.0.0.1:{server.server_port}'
    print(f'Score Arena Redline: {url}\nMantenha esta janela aberta. Ctrl+C para encerrar.', flush=True)
    if not args.no_browser:
        webbrowser.open(url)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.cancel_event.set()
        server.server_close()

if __name__ == '__main__':
    main()
