"""OpenAI LLM client implementation."""

from __future__ import annotations

from typing import TYPE_CHECKING

from app.clients.llm_client import LLMClientError

if TYPE_CHECKING:
    from openai import OpenAI


class OpenAIClientError(Exception):
    """Raised when the OpenAI client cannot be created."""


class OpenAIClient:
    """Generates text using OpenAI."""

    def __init__(self, sdk_client: "OpenAI") -> None:
        self._sdk_client = sdk_client

    def generate_text(self, *, prompt: str, model: str) -> str:
        try:
            response = self._sdk_client.responses.create(model=model, input=prompt)
        except Exception as error:
            raise LLMClientError("OpenAI failed to generate text.") from error

        output_text = getattr(response, "output_text", "")
        if isinstance(output_text, str) and output_text.strip():
            return output_text.strip()

        raise LLMClientError("OpenAI returned an empty response.")


class OpenAIClientFactory:
    """Creates configured OpenAI clients."""

    def create(self, api_key: str) -> OpenAIClient:
        try:
            from openai import OpenAI
        except ModuleNotFoundError as error:
            raise OpenAIClientError("OpenAI SDK is not installed. Install project dependencies first.") from error

        return OpenAIClient(OpenAI(api_key=api_key))
