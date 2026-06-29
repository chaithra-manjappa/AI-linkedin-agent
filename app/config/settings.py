"""Application settings."""

from __future__ import annotations

from dataclasses import dataclass
import os


class ConfigurationError(Exception):
    """Raised when application configuration is invalid."""


@dataclass(frozen=True, slots=True)
class Settings:
    """Runtime settings loaded from environment variables."""

    openai_api_key: str
    log_level: str = "INFO"

    @classmethod
    def from_environment(cls) -> "Settings":
        settings = cls(
            openai_api_key=os.getenv("OPENAI_API_KEY", "").strip(),
            log_level=os.getenv("LOG_LEVEL", "INFO").strip() or "INFO",
        )
        settings.validate()
        return settings

    def validate(self) -> None:
        if not self.openai_api_key:
            raise ConfigurationError("OPENAI_API_KEY is missing. Add it to .env or your shell environment.")
