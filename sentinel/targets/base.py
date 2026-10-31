"""The Target interface.

Keeping this as a tiny abstract base class means the evaluator is written
against `Target`, not against Ollama specifically. Swapping the mock for a
real model (or adding an OpenAI/Anthropic target later) touches only this
folder.
"""

from abc import ABC, abstractmethod


class Target(ABC):
    name: str = "target"

    @abstractmethod
    def generate(self, system: str, user: str) -> str:
        """Send a system + user message, return the model's text reply."""
        raise NotImplementedError
