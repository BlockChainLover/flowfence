"""Offline Gate A-D integration hooks; not a certified production runtime."""
import builtins
from contextlib import contextmanager
import io
from pathlib import Path
from threading import RLock
from types import MethodType

from src.experiments.aamas_gate_ac import MarbleBoundaryAdapter

_FILE_LOCK = RLock()


class ArtifactWriter(io.StringIO):
    """Publish a complete text artifact at flush/close, before shared storage sees it.

    Scope: the upstream coder's single synchronous `open(..., 'w').write(text)`.
    This is not an OS sandbox or a general transparent filesystem replacement.
    """
    def __init__(self, file, release):
        super().__init__()
        self.file = file
        self.release = release

    def flush(self):
        if self.closed:
            raise ValueError('I/O operation on closed file')
        safe = self.release(self.getvalue())
        self.file.seek(0)
        self.file.write(safe)
        self.file.truncate()
        self.file.flush()

    def close(self):
        if not self.closed:
            try:
                self.flush()
            finally:
                self.file.close()
                super().close()


@contextmanager
def coding_write_boundary(module, workspace, release):
    """Intercept the actual coder module's open; leave all read calls unchanged."""
    workspace = Path(workspace).resolve()
    with _FILE_LOCK:
        previous = module.__dict__.get('open')
        original = previous or builtins.open

        def scoped_open(path, mode='r', *args, **kwargs):
            file = original(path, mode, *args, **kwargs)
            if mode == 'w' and Path(path).resolve().is_relative_to(workspace):
                return ArtifactWriter(file, release)
            return file

        module.open = scoped_open
        try:
            yield
        finally:
            if previous is None:
                del module.open
            else:
                module.open = previous


class RecoveredMarbleAdapter(MarbleBoundaryAdapter):
    """Same optional write boundary in both defense arms, no gold or new detector."""
    def install(self):
        super().install()
        if self.engine.environment.name != 'Coding Environment':
            return
        from marble.environments.coding_utils import coder
        env = self.engine.environment
        old = env.apply_action

        def apply(obj, agent_id, action_name, arguments):
            with coding_write_boundary(
                coder, obj.workspace_dir,
                lambda text: self.release(text, agent_id, 'shared', 'shared_doc', 'WORKSPACE_WRITE'),
            ):
                return old(agent_id, action_name, arguments)
        self.wrap(env, 'apply_action', apply)


class CommunicationEdges:
    """Permission-only intervention; never mutates MARBLE graph/prompt/scheduler."""
    def __init__(self, agents, allowed):
        self.allowed = frozenset(tuple(edge) for edge in allowed)
        self.attempts = []
        ids = {a.agent_id for a in agents}
        if any(a not in ids or b not in ids or a == b for a, b in self.allowed):
            raise ValueError('invalid edge')
        for agent in agents:
            original_send, original_receive = agent.send_message, agent.receive_message
            def send(obj, session_id, target_agent, message, _old=original_send):
                self.check(obj.agent_id, target_agent.agent_id)
                return _old(session_id, target_agent, message)
            def receive(obj, session_id, from_agent, message, _old=original_receive):
                self.check(from_agent.agent_id, obj.agent_id)
                return _old(session_id, from_agent, message)
            agent.send_message = MethodType(send, agent)
            agent.receive_message = MethodType(receive, agent)

    def check(self, source, target):
        allowed = (source, target) in self.allowed
        self.attempts.append({'source': source, 'target': target, 'allowed': allowed})
        if not allowed:
            raise PermissionError('communication edge is not permitted')
