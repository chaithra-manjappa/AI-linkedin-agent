# Sprint 1

## Goal

Create the application foundation.

Requirements

- Create Settings class
- Read .env
- Validate API key
- Create OpenAI client
- Add logging
- Create app.py entry point
- Add proper type hints
- Handle missing API key gracefully

Do not implement any AI generation yet.

# Sprint 2 – LinkedIn Writer Agent

## Goal

Implement the first working AI feature that generates a LinkedIn post for a user-provided topic.

## Requirements

- Create `LinkedInWriterAgent` responsible only for content generation.
- Create `PromptService` to load Markdown prompt templates and replace placeholders.
- Store prompts in `app/prompts/` as `.md` files.
- Reuse the existing `OpenAIClient`.
- Create a `LinkedInPost` model for structured output.
- Update `app.py` to provide a simple CLI that accepts a topic and displays the generated post.
- Add logging for key application events.
- Handle missing API keys, invalid input, and OpenAI API errors gracefully.
- Add unit tests for `PromptService` and `WriterAgent` using mocked OpenAI responses.

## Constraints

- Do not implement research, memory, scheduling, publishing, or other future roadmap features.
- Do not hardcode prompts in Python code.
- Keep classes small and follow SOLID principles.
- Use the latest OpenAI Python SDK.


# Sprint 3 – Multi-Provider LLM Support

## Goal

Refactor the AI integration layer to support multiple LLM providers while keeping the application logic independent of the underlying provider.

## Requirements

- Create an abstract `LLMClient` interface.
- Implement `GroqClient` as the first provider.
- Keep the existing OpenAI implementation as an optional provider.
- Select the provider using the `LLM_PROVIDER` environment variable.
- Ensure `LinkedInWriterAgent` depends only on the `LLMClient` abstraction.
- Maintain existing functionality without changing the writer agent's behavior.
- Add unit tests for provider selection and client implementations.

## Constraints

- Follow SOLID principles.
- Avoid duplicating provider logic.
- Do not hardcode provider-specific code inside the writer agent.