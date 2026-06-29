"""OpenAI SDK client factory."""

from __future__ import annotations

from typing import TYPE_CHECKING

from app.config.settings import Settings

if TYPE_CHECKING:
    from openai import OpenAI


class OpenAIClientFactory:
    """Creates configured OpenAI SDK clients."""

    def create(self, settings: Settings) -> "OpenAI":
        from openai import OpenAI

        return OpenAI(api_key=settings.openai_api_key)
