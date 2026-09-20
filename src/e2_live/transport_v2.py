"""Prospective, allowlisted transport diagnostics. No retry or outcome repair."""
import json
import multiprocessing as mp
import re
import socket
import urllib.error
import urllib.request
from scripts.validate_e2_live_config import canonical


class TransportFailure(RuntimeError):
    def __init__(self, diagnostics):
        self.diagnostics = diagnostics
        super().__init__('PROVIDER_FAILURE')


def diagnostics(exc, request=None, key=''):
    """Do not serialize arbitrary exception messages, error bodies or headers."""
    cause = exc.reason if isinstance(exc, urllib.error.URLError) and isinstance(exc.reason, BaseException) else exc
    result = {'exception_class': type(exc).__name__, 'underlying_exception_class': type(cause).__name__,
              'http_status': None, 'provider_request_id': None, 'provider_error_code': None,
              'timeout': isinstance(cause, (TimeoutError, socket.timeout))}
    if isinstance(exc, urllib.error.HTTPError):
        result['http_status'] = exc.code if type(exc.code) is int else None
        headers = exc.headers or {}
        candidate = headers.get('x-request-id') or headers.get('request-id')
        serialized = canonical(request or {})
        if (isinstance(candidate, str) and re.fullmatch(r'[A-Za-z0-9_-]{8,100}', candidate)
                and candidate not in serialized and candidate not in key and (not key or key not in candidate)):
            result['provider_request_id'] = candidate
        try:
            body = json.loads(exc.read(65536))
            base = body.get('base_resp', {}) if isinstance(body, dict) else {}
            code = base.get('status_code') if isinstance(base, dict) else None
            if type(code) is int and 0 <= code <= 999999:
                result['provider_error_code'] = code
        except (ValueError, OSError, AttributeError):
            pass
    return result


def provider_worker(conn, request, key, timeout):
    try:
        headers = dict(request['headers'], Authorization='Bearer ' + key)
        req = urllib.request.Request(request['url'], data=canonical(request['json']).encode(), headers=headers, method='POST')
        class NoRedirect(urllib.request.HTTPRedirectHandler):
            def redirect_request(self, *args, **kwargs):
                return None
        with urllib.request.build_opener(NoRedirect).open(req, timeout=timeout) as response:
            value = {'body': json.loads(response.read().decode('utf-8')),
                     'headers': dict(response.headers), 'http_status': response.status}
        conn.send(('ok', value))
    except BaseException as exc:
        conn.send(('error', diagnostics(exc, request, key)))
    finally:
        conn.close()


def supervised_provider(request, key, timeout):
    ctx = mp.get_context('spawn')
    receive, send = ctx.Pipe(duplex=False)
    process = ctx.Process(target=provider_worker, args=(send, request, key, timeout))
    process.start()
    send.close()
    try:
        if not receive.poll(timeout):
            process.terminate(); process.join(5)
            if process.is_alive():
                process.kill(); process.join()
            raise TransportFailure(diagnostics(TimeoutError()))
        try:
            status, value = receive.recv()
        except EOFError:
            raise TransportFailure(diagnostics(RuntimeError())) from None
        process.join(5)
        if process.is_alive():
            process.terminate(); process.join()
            raise TransportFailure(diagnostics(RuntimeError()))
        if status != 'ok':
            raise TransportFailure(value)
        return value
    finally:
        receive.close()
        if process.is_alive():
            process.terminate(); process.join()


class LiveProviderV2:
    def __init__(self, key):
        self.key = key

    def call(self, request, timeout):
        return supervised_provider(request, self.key, timeout)
