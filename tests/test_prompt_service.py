from pathlib import Path
import tempfile
import unittest

from app.services.prompt_service import PromptService, PromptTemplateError


class PromptServiceTest(unittest.TestCase):
    def test_render_replaces_markdown_placeholders(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            prompts_dir = Path(temp_dir)
            (prompts_dir / "template.md").write_text("Topic: {{ topic }}", encoding="utf-8")

            rendered = PromptService(prompts_dir).render("template.md", {"topic": "AI workflows"})

        self.assertEqual(rendered, "Topic: AI workflows")

    def test_render_raises_for_missing_placeholder_value(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            prompts_dir = Path(temp_dir)
            (prompts_dir / "template.md").write_text("Topic: {{ topic }}", encoding="utf-8")

            with self.assertRaises(PromptTemplateError):
                PromptService(prompts_dir).render("template.md", {})

    def test_render_raises_for_non_markdown_template(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            with self.assertRaises(PromptTemplateError):
                PromptService(Path(temp_dir)).render("template.txt", {})


if __name__ == "__main__":
    unittest.main()
