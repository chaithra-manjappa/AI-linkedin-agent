"""Application settings."""

from __future__ import annotations

from dataclasses import dataclass
import os


class ConfigurationError(Exception):
    """Raised when application configuration is invalid."""


@dataclass(frozen=True, slots=True)
class Settings:
    """Runtime settings loaded from environment variables."""

    llm_provider: str
    llm_api_key: str
    llm_model: str
    log_level: str = "INFO"

    @classmethod
    def from_environment(cls) -> "Settings":
        provider = os.getenv("LLM_PROVIDER", "groq").strip().lower() or "groq"
        settings = cls(
            llm_provider=provider,
            llm_api_key=cls._api_key_for_provider(provider),
            llm_model=cls._model_for_provider(provider),
            log_level=os.getenv("LOG_LEVEL", "INFO").strip() or "INFO",
        )
        settings.validate()
        return settings

    def validate(self) -> None:
        if self.llm_provider not in {"groq", "openai"}:
            raise ConfigurationError("LLM_PROVIDER must be one of: groq, openai.")
        if not self.llm_api_key:
            env_name = "GROQ_API_KEY" if self.llm_provider == "groq" else "OPENAI_API_KEY"
            raise ConfigurationError(f"{env_name} is missing. Add it to .env or your shell environment.")
        if not self.llm_model.strip():
            raise ConfigurationError("LLM model cannot be empty.")

    @staticmethod
    def _api_key_for_provider(provider: str) -> str:
        if provider == "openai":
            return os.getenv("OPENAI_API_KEY", "").strip()

        return os.getenv("GROQ_API_KEY", "").strip()

    @staticmethod
    def _model_for_provider(provider: str) -> str:
        explicit_model = os.getenv("LLM_MODEL", "").strip()
        if explicit_model:
            return explicit_model

        if provider == "openai":
            return os.getenv("OPENAI_MODEL", "gpt-5.5").strip() or "gpt-5.5"

        return os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile").strip() or "llama-3.3-70b-versatile"
