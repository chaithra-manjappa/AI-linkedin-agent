from pathlib import Path
import tempfile
import unittest

from app.clients.llm_client import LLMClientError
from app.agents.linkedin_writer_agent import ContentGenerationError, LinkedInWriterAgent
from app.services.prompt_service import PromptService


class FakeLLMClient:
    def __init__(self, response: str = "Generated post", error: Exception | None = None) -> None:
        self.response = response
        self.error = error
        self.created_with: dict[str, str] | None = None

    def generate_text(self, *, prompt: str, model: str) -> str:
        self.created_with = {"model": model, "prompt": prompt}
        if self.error:
            raise self.error
        return self.response


class LinkedInWriterAgentTest(unittest.TestCase):
    def test_generate_returns_structured_post(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            prompts_dir = Path(temp_dir)
            (prompts_dir / "linkedin_post.md").write_text("Write about {{ topic }}", encoding="utf-8")
            client = FakeLLMClient("Generated post")
            agent = LinkedInWriterAgent(
                client=client,
                prompt_service=PromptService(prompts_dir),
                model="test-model",
            )

            post = agent.generate("AI code review")

        self.assertEqual(post.topic, "AI code review")
        self.assertEqual(post.content, "Generated post")
        self.assertEqual(client.created_with, {"model": "test-model", "prompt": "Write about AI code review"})

    def test_generate_rejects_empty_topic(self) -> None:
        agent = LinkedInWriterAgent(
            client=FakeLLMClient(),
            prompt_service=PromptService(Path("unused")),
            model="test-model",
        )

        with self.assertRaises(ValueError):
            agent.generate("  ")

    def test_generate_wraps_openai_errors(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            prompts_dir = Path(temp_dir)
            (prompts_dir / "linkedin_post.md").write_text("Write about {{ topic }}", encoding="utf-8")
            agent = LinkedInWriterAgent(
                client=FakeLLMClient(error=LLMClientError("api unavailable")),
                prompt_service=PromptService(prompts_dir),
                model="test-model",
            )

            with self.assertRaises(ContentGenerationError):
                agent.generate("AI strategy")


if __name__ == "__main__":
    unittest.main()
