import os
from unittest.mock import patch
import unittest

from app.config.settings import ConfigurationError, Settings


class SettingsTest(unittest.TestCase):
    def test_loads_groq_provider_by_default(self) -> None:
        with patch.dict(os.environ, {"GROQ_API_KEY": "groq-key"}, clear=True):
            settings = Settings.from_environment()

        self.assertEqual(settings.llm_provider, "groq")
        self.assertEqual(settings.llm_api_key, "groq-key")
        self.assertEqual(settings.llm_model, "llama-3.3-70b-versatile")

    def test_loads_openai_provider_when_selected(self) -> None:
        env = {
            "LLM_PROVIDER": "openai",
            "OPENAI_API_KEY": "openai-key",
            "OPENAI_MODEL": "gpt-test",
        }
        with patch.dict(os.environ, env, clear=True):
            settings = Settings.from_environment()

        self.assertEqual(settings.llm_provider, "openai")
        self.assertEqual(settings.llm_api_key, "openai-key")
        self.assertEqual(settings.llm_model, "gpt-test")

    def test_rejects_unknown_provider(self) -> None:
        with patch.dict(os.environ, {"LLM_PROVIDER": "unknown"}, clear=True):
            with self.assertRaises(ConfigurationError):
                Settings.from_environment()

    def test_rejects_missing_provider_api_key(self) -> None:
        with patch.dict(os.environ, {"LLM_PROVIDER": "groq"}, clear=True):
            with self.assertRaises(ConfigurationError):
                Settings.from_environment()


if __name__ == "__main__":
    unittest.main()
