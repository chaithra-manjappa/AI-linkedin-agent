import unittest

from app.clients.factory import LLMClientFactory, LLMClientFactoryError
from app.config.settings import Settings


class FakeProviderFactory:
    def __init__(self, client: object) -> None:
        self.client = client
        self.created_with: str | None = None

    def create(self, api_key: str) -> object:
        self.created_with = api_key
        return self.client


class LLMClientFactoryTest(unittest.TestCase):
    def test_selects_groq_provider(self) -> None:
        groq_client = object()
        groq_factory = FakeProviderFactory(groq_client)
        openai_factory = FakeProviderFactory(object())

        client = LLMClientFactory(groq_factory=groq_factory, openai_factory=openai_factory).create(
            Settings(llm_provider="groq", llm_api_key="groq-key", llm_model="test-model")
        )

        self.assertIs(client, groq_client)
        self.assertEqual(groq_factory.created_with, "groq-key")
        self.assertIsNone(openai_factory.created_with)

    def test_selects_openai_provider(self) -> None:
        openai_client = object()
        groq_factory = FakeProviderFactory(object())
        openai_factory = FakeProviderFactory(openai_client)

        client = LLMClientFactory(groq_factory=groq_factory, openai_factory=openai_factory).create(
            Settings(llm_provider="openai", llm_api_key="openai-key", llm_model="test-model")
        )

        self.assertIs(client, openai_client)
        self.assertEqual(openai_factory.created_with, "openai-key")
        self.assertIsNone(groq_factory.created_with)

    def test_rejects_unsupported_provider(self) -> None:
        with self.assertRaises(LLMClientFactoryError):
            LLMClientFactory().create(Settings(llm_provider="bad", llm_api_key="key", llm_model="model"))


if __name__ == "__main__":
    unittest.main()
