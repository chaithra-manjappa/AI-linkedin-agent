"""LinkedIn post domain model."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class LinkedInPost:
    """Generated LinkedIn post content."""

    topic: str
    content: str

    def __post_init__(self) -> None:
        if not self.topic.strip():
            raise ValueError("LinkedIn post topic cannot be empty.")
        if not self.content.strip():
            raise ValueError("LinkedIn post content cannot be empty.")
