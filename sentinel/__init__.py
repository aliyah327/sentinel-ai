"""Sentinel-AI: a small, auditable LLM red-teaming harness.

The package is deliberately split so each concern lives in one place:

    targets/     -> things we send prompts to (a mock, or local Ollama)
    probes/      -> attack inputs (the raw jailbreak/injection attempts)
    detectors/   -> decide whether a single response is a failure
    evaluators/  -> run probes x strategies x repeats and score the run
    reporting/   -> turn results into JSON + HTML evidence

Nothing here produces harmful content. The whole benchmark is built around
a *canary token*: a secret string placed in the system prompt that the model
is told never to reveal. An attack "succeeds" only when the model leaks that
token. This lets us measure prompt-injection / jailbreak robustness without
ever asking the model for dangerous information.
"""

__version__ = "0.1.0"
