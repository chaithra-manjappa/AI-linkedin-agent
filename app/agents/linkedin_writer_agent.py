"""LinkedIn writer agent."""

from __future__ import annotations

from app.clients.llm_client import LLMClient, LLMClientError
from app.models.linkedin_post import LinkedInPost
from app.services.prompt_service import PromptService


class ContentGenerationError(Exception):
    """Raised when LinkedIn post generation fails."""


class LinkedInWriterAgent:
    """Generates LinkedIn posts from user-provided topics."""

    _template_name = "linkedin_post.md"

    def __init__(self, client: LLMClient, prompt_service: PromptService, model: str) -> None:
        self._client = client
        self._prompt_service = prompt_service
        self._model = model

    def generate(self, topic: str) -> LinkedInPost:
        normalized_topic = topic.strip()
        if not normalized_topic:
            raise ValueError("Topic cannot be empty.")

        prompt = self._prompt_service.render(self._template_name, {"topic": normalized_topic})

        try:
            content = self._client.generate_text(model=self._model, prompt=prompt)
        except LLMClientError as error:
            raise ContentGenerationError("LLM provider failed to generate a LinkedIn post.") from error

        return LinkedInPost(topic=normalized_topic, content=content)
