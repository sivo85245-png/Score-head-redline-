import io
import json
import threading
import queue
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch
from servidor import Handler
from dados import carregar, CENARIOS


def call(path, method='GET', origin=None, server=None):
    h = object.__new__(Handler)
    h.path = path
    h.headers = {'Host': '127.0.0.1:8765'}
    if origin:
        h.headers['Origin'] = origin
    h.wfile = io.BytesIO()
    h.server = server or SimpleNamespace(measure_lock=threading.Lock(), cancel_event=threading.Event(), job_state={'estado': 'pronto'})
    h.send_response = lambda status: setattr(h, 'status', status)
    h.send_header = lambda *args: None
    h.end_headers = lambda: None
    getattr(h, 'do_' + method)()
    return h.status, h.wfile.getvalue()


class TestRedline(unittest.TestCase):
    def test_copia_offline_exata(self):
        data = json.loads((Path(__file__).parent/'web/datasets.js').read_text(encoding='utf-8').removeprefix('window.APS_DATA=').strip().removesuffix(';'))
        self.assertEqual(len(set(data['names'])), 20000)
        for label, key in CENARIOS.items():
            original = carregar(label)
            rebuilt = [(f'Player_{id:05}', score) for id, score in data['scenarios'][key]]
            self.assertEqual(rebuilt, original)

    def test_arquivos_e_rotas(self):
        for path in ('/', '/style.css', '/app.js', '/render.js', '/engine.js', '/datasets.js', '/api/health'):
            self.assertEqual(call(path)[0], 200)
        self.assertEqual(call('/../algoritmos.py')[0], 404)
        self.assertEqual(call('/api/benchmark', 'POST', 'http://other.test')[0], 403)

    def test_tarefa_assincrona(self):
        server = SimpleNamespace(measure_lock=threading.Lock(), cancel_event=threading.Event(), job_state={'estado': 'pronto'})
        with patch('servidor.threading.Thread') as thread:
            status, body = call('/api/benchmark', 'POST', server=server)
            self.assertEqual(status, 202)
            thread.return_value.start.assert_called_once()
            self.assertEqual(call('/api/benchmark', 'POST', server=server)[0], 409)
            self.assertEqual(json.loads(call('/api/benchmark', server=server)[1])['estado'], 'executando')
            self.assertEqual(call('/api/cancelar', 'POST', server=server)[0], 200)
            self.assertTrue(server.cancel_event.is_set())
            server.measure_lock.release()

    def test_worker_publica_resultados(self):
        from servidor import processo_medicao
        fila = queue.Queue()
        with patch('servidor.executar', return_value={'resultados': []}) as execute, patch('servidor.salvar') as save:
            processo_medicao(SimpleNamespace(send=fila.put), threading.Event(), True)
            self.assertEqual(execute.call_args.kwargs['tamanhos'], (2500, 5000, 10000, 20000))
            save.assert_called_once()
        self.assertEqual(fila.get()['estado'], 'concluido')

    def test_processo_real_cancelamento(self):
        import multiprocessing
        from servidor import executar_trabalho
        evento = multiprocessing.get_context('spawn').Event()
        evento.set()
        server = SimpleNamespace(measure_lock=threading.Lock(), cancel_event=evento, job_state={})
        server.measure_lock.acquire()
        executar_trabalho(server, False)
        self.assertEqual(server.job_state['estado'], 'cancelado', server.job_state)
        self.assertFalse(server.measure_lock.locked())


if __name__ == '__main__':
    unittest.main(verbosity=2)
