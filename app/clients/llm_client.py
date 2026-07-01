"""Provider-neutral LLM client contracts."""

from __future__ import annotations

from typing import Protocol


class LLMClientError(Exception):
    """Raised when an LLM provider request fails."""


class LLMClient(Protocol):
    """Generates text with an underlying LLM provider."""

    def generate_text(self, *, prompt: str, model: str) -> str:
        """Generate text for a prompt."""
