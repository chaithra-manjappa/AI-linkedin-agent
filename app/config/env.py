"""Minimal .env loader for local configuration."""

from __future__ import annotations

import os
from pathlib import Path


class EnvFileLoader:
    """Loads simple KEY=VALUE pairs into the process environment."""

    def __init__(self, env_file: Path) -> None:
        self._env_file = env_file

    def load(self) -> None:
        if not self._env_file.exists():
            return

        for raw_line in self._env_file.read_text(encoding="utf-8").splitlines():
            line = raw_line.strip()

            if not line or line.startswith("#") or "=" not in line:
                continue

            key, value = line.split("=", 1)
            key = key.strip()

            if not key:
                continue

            os.environ.setdefault(key, self._normalize_value(value))

    @staticmethod
    def _normalize_value(value: str) -> str:
        normalized = value.strip()

        if len(normalized) >= 2 and normalized[0] == normalized[-1] and normalized[0] in {"'", '"'}:
            return normalized[1:-1]

        return normalized
