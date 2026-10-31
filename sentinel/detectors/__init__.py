"""Detectors: decide whether ONE response is a security failure.

A detector takes the response text (plus context like the canary value) and
returns a verdict dict:

    {"failed": True/False, "reason": "...", "detector": "canary_leak"}

'failed' here means 'the guardrail failed', i.e. the attack succeeded. We
separate detection from scoring so you can add new detectors without touching
the evaluator.
"""

from .canary import CanaryLeakDetector
from .refusal import RefusalDetector

__all__ = ["CanaryLeakDetector", "RefusalDetector", "build_detector"]


def build_detector(spec: dict):
    dtype = spec.get("type", "canary_leak")
    if dtype == "canary_leak":
        return CanaryLeakDetector(canary=spec["canary"])
    if dtype == "refusal":
        return RefusalDetector()
    raise ValueError(f"Unknown detector type: {dtype!r}")
