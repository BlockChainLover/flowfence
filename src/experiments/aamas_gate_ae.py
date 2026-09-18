"""Gate A-E generic-boundary feasibility probes, not a formal E2 adapter.

Explicit scope is intentionally required: the benchmark's unlabelled common
completion API cannot itself infer the receiving principal or evaluator spans.
"""
import builtins
from contextlib import contextmanager
from contextvars import ContextVar
from copy import deepcopy
from pathlib import Path

from src.experiments.aamas_gate_ad import ArtifactWriter


class ContextBoundaryProbe:
    def __init__(self, adapter, transport):
        self.adapter = adapter
        self.transport = transport
        self.principal = ContextVar('gate_ae_context_principal', default=None)
        self.calls = []

    @contextmanager
    def scope(self, recipient):
        token = self.principal.set(recipient)
        try:
            yield
        finally:
            self.principal.reset(token)

    def __call__(self, *args, **kwargs):
        recipient = self.principal.get()
        if recipient is None:
            raise RuntimeError('model recipient has no trusted runtime binding')
        safe = deepcopy(kwargs)
        for message in safe.get('messages', []):
            if isinstance(message.get('content'), str):
                message['content'] = self.adapter.release(
                    message['content'], 'runtime', recipient, 'private_memory', 'MEMORY_READ')
        self.calls.append({'recipient': recipient, 'messages_changed': safe.get('messages') != kwargs.get('messages')})
        return self.transport(*args, **safe)


@contextmanager
def workspace_publication_probe(workspace, release):
    """One namespace-based boundary for all active text writers, no handler list.

    Only the pinned synchronous open(...,'w') publication pattern is supported.
    No claim about arbitrary syscalls, concurrent writers or unregistered tools.
    """
    root = Path(workspace).resolve()
    original = builtins.open

    def opened(path, mode='r', *args, **kwargs):
        file = original(path, mode, *args, **kwargs)
        if isinstance(path, (str, bytes, Path)) and mode == 'w' and Path(path).resolve().is_relative_to(root):
            return ArtifactWriter(file, release)
        return file

    builtins.open = opened
    try:
        yield
    finally:
        builtins.open = original
