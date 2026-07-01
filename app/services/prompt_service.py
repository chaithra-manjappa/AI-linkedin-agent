"""Prompt template loading and rendering."""

from __future__ import annotations

from pathlib import Path
import re


class PromptTemplateError(Exception):
    """Raised when a prompt template cannot be loaded or rendered."""


class PromptService:
    """Loads Markdown prompt templates and replaces placeholders."""

    _placeholder_pattern = re.compile(r"{{\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*}}")

    def __init__(self, prompts_dir: Path) -> None:
        self._prompts_dir = prompts_dir

    def render(self, template_name: str, placeholders: dict[str, str]) -> str:
        template = self._load_template(template_name)

        def replace(match: re.Match[str]) -> str:
            key = match.group(1)
            if key not in placeholders:
                raise PromptTemplateError(f"Missing prompt placeholder value: {key}")
            return placeholders[key]

        rendered = self._placeholder_pattern.sub(replace, template)
        if not rendered.strip():
            raise PromptTemplateError(f"Prompt template is empty after rendering: {template_name}")

        return rendered

    def _load_template(self, template_name: str) -> str:
        template_path = self._prompts_dir / template_name

        if template_path.suffix != ".md":
            raise PromptTemplateError("Prompt templates must be Markdown files.")
        if not template_path.exists():
            raise PromptTemplateError(f"Prompt template not found: {template_name}")

        return template_path.read_text(encoding="utf-8")
