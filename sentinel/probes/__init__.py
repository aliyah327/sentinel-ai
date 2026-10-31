"""Probes + strategies.

Vocabulary (matches the training handout):
  - probe     : a base attack input with an intent, e.g. "get the secret".
  - strategy  : a transform applied to a probe's text to try to slip it past
                filters, e.g. base64 / rot13 / leetspeak. (Garak calls these
                "buffs"; Promptfoo calls them "strategies".)

A single probe expands into several concrete *test cases* — one per strategy.
"""

from .library import load_probes
from .strategies import STRATEGIES, apply_strategy

__all__ = ["load_probes", "STRATEGIES", "apply_strategy"]
