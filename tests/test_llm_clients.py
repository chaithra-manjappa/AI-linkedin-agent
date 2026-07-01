from types import SimpleNamespace
import unittest

from app.clients.groq_client import GroqClient
from app.clients.llm_client import LLMClientError
from app.clients.openai_client import OpenAIClient


class FakeOpenAIResponses:
    def __init__(self, response: object | None = None, error: Exception | None = None) -> None:
        self.response = response
        self.error = error
        self.created_with: dict[str, str] | None = None

    def create(self, *, model: str, input: str) -> object:
        self.created_with = {"model": model, "input": input}
        if self.error:
            raise self.error
        return self.response


class FakeGroqCompletions:
    def __init__(self, response: object | None = None, error: Exception | None = None) -> None:
        self.response = response
        self.error = error
        self.created_with: dict[str, object] | None = None

    def create(self, *, model: str, messages: list[dict[str, str]]) -> object:
        self.created_with = {"model": model, "messages": messages}
        if self.error:
            raise self.error
        return self.response


class LLMClientsTest(unittest.TestCase):
    def test_openai_client_generates_text(self) -> None:
        responses = FakeOpenAIResponses(SimpleNamespace(output_text=" Generated post "))
        sdk_client = SimpleNamespace(responses=responses)

        text = OpenAIClient(sdk_client).generate_text(prompt="Prompt", model="openai-model")

        self.assertEqual(text, "Generated post")
        self.assertEqual(responses.created_with, {"model": "openai-model", "input": "Prompt"})

    def test_openai_client_wraps_provider_errors(self) -> None:
        responses = FakeOpenAIResponses(error=RuntimeError("unavailable"))
        sdk_client = SimpleNamespace(responses=responses)

        with self.assertRaises(LLMClientError):
            OpenAIClient(sdk_client).generate_text(prompt="Prompt", model="openai-model")

    def test_groq_client_generates_text(self) -> None:
        response = SimpleNamespace(choices=[SimpleNamespace(message=SimpleNamespace(content=" Generated post "))])
        completions = FakeGroqCompletions(response)
        sdk_client = SimpleNamespace(chat=SimpleNamespace(completions=completions))

        text = GroqClient(sdk_client).generate_text(prompt="Prompt", model="groq-model")

        self.assertEqual(text, "Generated post")
        self.assertEqual(
            completions.created_with,
            {"model": "groq-model", "messages": [{"role": "user", "content": "Prompt"}]},
        )

    def test_groq_client_wraps_provider_errors(self) -> None:
        completions = FakeGroqCompletions(error=RuntimeError("unavailable"))
        sdk_client = SimpleNamespace(chat=SimpleNamespace(completions=completions))

        with self.assertRaises(LLMClientError):
            GroqClient(sdk_client).generate_text(prompt="Prompt", model="groq-model")


if __name__ == "__main__":
    unittest.main()
