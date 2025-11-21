from .base_ai_provider import AIProvider


class NoopAIProvider(AIProvider):
    """Deterministic provider used for tests and offline runs."""

    def complete(self, prompt: str) -> str:
        return f"[noop-ai] {prompt}"

    def chat(self, messages: list[dict]) -> str:
        summary = " | ".join(f"{m.get('role')}: {m.get('content')}" for m in messages)
        return f"[noop-ai-chat] {summary}"
