"""Groq LLM client implementation."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from app.clients.llm_client import LLMClientError

if TYPE_CHECKING:
    from groq import Groq


class GroqClientError(Exception):
    """Raised when the Groq client cannot be created."""


class GroqClient:
    """Generates text using Groq chat completions."""

    def __init__(self, sdk_client: "Groq") -> None:
        self._sdk_client = sdk_client

    def generate_text(self, *, prompt: str, model: str) -> str:
        try:
            response = self._sdk_client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
            )
        except Exception as error:
            raise LLMClientError("Groq failed to generate text.") from error

        content = self._extract_content(response)
        if content:
            return content

        raise LLMClientError("Groq returned an empty response.")

    @staticmethod
    def _extract_content(response: Any) -> str:
        choices = getattr(response, "choices", None)
        if not choices:
            return ""

        message = getattr(choices[0], "message", None)
        content = getattr(message, "content", "")
        if isinstance(content, str):
            return content.strip()

        return ""


class GroqClientFactory:
    """Creates configured Groq clients."""

    def create(self, api_key: str) -> GroqClient:
        try:
            from groq import Groq
        except ModuleNotFoundError as error:
            raise GroqClientError("Groq SDK is not installed. Install project dependencies first.") from error

        return GroqClient(Groq(api_key=api_key))
