from typing import Protocol


class AIProvider(Protocol):
    def complete(self, prompt: str) -> str:
        ...

    def chat(self, messages: list[dict]) -> str:
        ...
