"""LLM provider selection."""

from __future__ import annotations

from app.clients.groq_client import GroqClientFactory
from app.clients.llm_client import LLMClient
from app.clients.openai_client import OpenAIClientFactory
from app.config.settings import Settings


class LLMClientFactoryError(Exception):
    """Raised when an LLM client cannot be selected or created."""


class LLMClientFactory:
    """Creates the configured LLM provider client."""

    def __init__(
        self,
        groq_factory: GroqClientFactory | None = None,
        openai_factory: OpenAIClientFactory | None = None,
    ) -> None:
        self._groq_factory = groq_factory or GroqClientFactory()
        self._openai_factory = openai_factory or OpenAIClientFactory()

    def create(self, settings: Settings) -> LLMClient:
        if settings.llm_provider == "groq":
            return self._groq_factory.create(settings.llm_api_key)
        if settings.llm_provider == "openai":
            return self._openai_factory.create(settings.llm_api_key)

        raise LLMClientFactoryError(f"Unsupported LLM provider: {settings.llm_provider}")
