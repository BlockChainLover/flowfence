"""Minimal MiniMax-only client for MAS smoke runs."""

from __future__ import annotations

import json
import os
import time
import urllib.error
import urllib.request
from dataclasses import dataclass
from typing import Any

from src.runtime.events import sha256_text


DEFAULT_BASE_URL = "https://api.minimaxi.com/v1"
DEFAULT_MODEL = "MiniMax-M2.7"


@dataclass(frozen=True)
class MiniMaxSettings:
    api_key: str | None
    base_url: str
    model: str
    group_id: str | None


class MiniMaxClient:
    """Small OpenAI-compatible MiniMax chat-completion wrapper.

    Credentials are read only from environment variables. Secret values are
    never included in raised errors or returned metadata.
    """

    def __init__(
        self,
        model: str | None = None,
        timeout_seconds: float = 60.0,
        temperature: float = 0.0,
        max_tokens: int = 256,
    ) -> None:
        self.timeout_seconds = float(timeout_seconds)
        self.temperature = float(temperature)
        self.max_tokens = int(max_tokens)
        env_model = os.environ.get("MODEL_MINIMAX27") or os.environ.get("MINIMAX_MODEL") or DEFAULT_MODEL
        self.settings = MiniMaxSettings(
            api_key=os.environ.get("MINIMAX_API_KEY"),
            base_url=(os.environ.get("MINIMAX_BASE_URL") or DEFAULT_BASE_URL).rstrip("/"),
            model=model or env_model,
            group_id=os.environ.get("MINIMAX_GROUP_ID"),
        )

    @property
    def model(self) -> str:
        return self.settings.model

    def missing_variables(self) -> list[str]:
        missing: list[str] = []
        if not self.settings.api_key:
            missing.append("MINIMAX_API_KEY")
        if not self.settings.base_url:
            missing.append("MINIMAX_BASE_URL")
        if not self.settings.model:
            missing.append("MODEL_MINIMAX27 or MINIMAX_MODEL")
        return missing

    def available(self) -> bool:
        return not self.missing_variables()

    def complete(self, prompt: str) -> dict[str, Any]:
        missing = self.missing_variables()
        if missing:
            raise RuntimeError(f"MiniMax credentials unavailable; missing: {', '.join(missing)}")
        payload = {
            "model": self.settings.model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
        }
        data = json.dumps(payload).encode("utf-8")
        headers = {
            "Authorization": "Bearer " + str(self.settings.api_key),
            "Content-Type": "application/json",
        }
        if self.settings.group_id:
            headers["X-Group-Id"] = self.settings.group_id
        request = urllib.request.Request(
            self.settings.base_url + "/chat/completions",
            data=data,
            headers=headers,
            method="POST",
        )
        started = time.perf_counter()
        try:
            with urllib.request.urlopen(request, timeout=self.timeout_seconds) as response:
                raw = response.read().decode("utf-8")
        except urllib.error.URLError as exc:
            raise RuntimeError("MiniMax request failed without exposing credentials") from exc
        latency = time.perf_counter() - started
        body = json.loads(raw)
        choices = body.get("choices") if isinstance(body, dict) else None
        text = ""
        if choices:
            message = choices[0].get("message") if isinstance(choices[0], dict) else {}
            text = str(message.get("content") or choices[0].get("text") or "")
        return {
            "text": text,
            "provider": "minimax",
            "model": self.settings.model,
            "prompt_sha256": sha256_text(prompt),
            "response_sha256": sha256_text(text),
            "usage": body.get("usage") if isinstance(body, dict) else None,
            "latency_seconds": latency,
        }
