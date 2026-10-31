"""Targets: anything Sentinel can send a prompt to and get text back.

Every target implements one method:  generate(system, user) -> str

Two targets ship with the tool:
  - MockTarget:   no network, no model. Simulates a guardrailed assistant
                  that leaks its canary only against certain attack shapes.
                  This makes the whole tool runnable and gradeable with zero
                  installs, and gives deterministic output for the demo.
  - OllamaTarget: talks to a local Ollama server (http://127.0.0.1:11434).
                  Same interface, so the evaluator does not care which one
                  it is driving.
"""

from .base import Target
from .mock import MockTarget
from .ollama import OllamaTarget


def build_target(spec: dict) -> Target:
    """Factory: turn a config dict into a Target instance.

    spec example:  {"type": "mock"}  or
                   {"type": "ollama", "model": "llama3.2",
                    "base_url": "http://127.0.0.1:11434"}
    """
    ttype = spec.get("type", "mock").lower()
    if ttype == "mock":
        return MockTarget(canary=spec.get("canary", "CANARY-7F3A-SECRET"))
    if ttype == "ollama":
        return OllamaTarget(
            model=spec.get("model", "llama3.2"),
            base_url=spec.get("base_url", "http://127.0.0.1:11434"),
            timeout=spec.get("timeout", 120),
        )
    raise ValueError(f"Unknown target type: {ttype!r}")
