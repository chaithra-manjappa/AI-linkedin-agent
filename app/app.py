"""Application entry point."""

from __future__ import annotations

import argparse
import logging
from pathlib import Path
import sys

from app.agents.linkedin_writer_agent import ContentGenerationError, LinkedInWriterAgent
from app.clients.factory import LLMClientFactory, LLMClientFactoryError
from app.clients.groq_client import GroqClientError
from app.clients.openai_client import OpenAIClientError
from app.config.env import EnvFileLoader
from app.config.settings import ConfigurationError, Settings
from app.services.prompt_service import PromptService, PromptTemplateError
from app.utils.logging import configure_logging


LOGGER = logging.getLogger(__name__)
PROMPTS_DIR = Path(__file__).resolve().parent / "prompts"


def bootstrap(topic: str, env_file: Path | None = None) -> int:
    """Load configuration, generate a LinkedIn post, and display it."""

    EnvFileLoader(env_file or Path(".env")).load()

    try:
        settings = Settings.from_environment()
        configure_logging(settings.log_level)
        client = LLMClientFactory().create(settings)
        agent = LinkedInWriterAgent(
            client=client,
            prompt_service=PromptService(PROMPTS_DIR),
            model=settings.llm_model,
        )
        LOGGER.info("Generating LinkedIn post with %s.", settings.llm_provider)
        post = agent.generate(topic)
    except (
        ConfigurationError,
        LLMClientFactoryError,
        GroqClientError,
        OpenAIClientError,
        ValueError,
        PromptTemplateError,
        ContentGenerationError,
    ) as error:
        configure_logging("INFO")
        LOGGER.error("%s", error)
        return 1

    LOGGER.info("LinkedIn post generated.")
    print(post.content)
    return 0


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate a LinkedIn post for a topic.")
    parser.add_argument("topic", nargs="*", help="Topic to write about.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv if argv is not None else sys.argv[1:])
    topic = " ".join(args.topic).strip()
    if not topic:
        configure_logging("INFO")
        LOGGER.error("Topic is required.")
        return 1

    return bootstrap(topic)


if __name__ == "__main__":
    raise SystemExit(main())
