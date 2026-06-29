"""Application entry point for Sprint 1."""

from __future__ import annotations

import logging
from pathlib import Path

from app.clients.openai_client import OpenAIClientFactory
from app.config.env import EnvFileLoader
from app.config.settings import ConfigurationError, Settings
from app.utils.logging import configure_logging


LOGGER = logging.getLogger(__name__)


def bootstrap(env_file: Path | None = None) -> int:
    """Load configuration and initialize external clients."""

    EnvFileLoader(env_file or Path(".env")).load()

    try:
        settings = Settings.from_environment()
        configure_logging(settings.log_level)
        OpenAIClientFactory().create(settings)
    except ConfigurationError as error:
        configure_logging("INFO")
        LOGGER.error("%s", error)
        return 1

    LOGGER.info("Application foundation initialized.")
    return 0


def main() -> int:
    return bootstrap()


if __name__ == "__main__":
    raise SystemExit(main())
