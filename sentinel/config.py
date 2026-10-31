"""Config loading.

We support YAML if PyYAML is installed, and fall back to JSON otherwise, so
the tool runs with zero third-party dependencies but still reads the nice
YAML configs when the library is present. A `.json` config always works.
"""

import json
import os


def load_config(path: str) -> dict:
    if not os.path.exists(path):
        raise FileNotFoundError(f"Config not found: {path}")

    text = open(path, "r", encoding="utf-8").read()

    if path.endswith((".yaml", ".yml")):
        try:
            import yaml  # PyYAML, optional
            return yaml.safe_load(text)
        except ImportError:
            raise SystemExit(
                "This config is YAML but PyYAML isn't installed.\n"
                "Either run:  pip install pyyaml\n"
                "or use the equivalent .json config instead."
            )
    return json.loads(text)


def apply_overrides(config: dict, args) -> dict:
    """CLI flags win over file values, so the demo can tweak one thing fast."""
    if getattr(args, "target", None):
        config.setdefault("target", {})["type"] = args.target
    if getattr(args, "model", None):
        config.setdefault("target", {})["type"] = "ollama"
        config["target"]["model"] = args.model
    if getattr(args, "repeat", None):
        config["repeat"] = args.repeat
    if getattr(args, "strategies", None):
        config["strategies"] = [s.strip() for s in args.strategies.split(",")]

    # Make sure a canary always exists and is shared with the target + detector.
    config.setdefault("canary", "CANARY-7F3A-SECRET")
    config.setdefault("target", {"type": "mock"})
    config["target"].setdefault("canary", config["canary"])
    return config
