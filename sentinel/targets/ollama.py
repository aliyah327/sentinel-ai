"""OllamaTarget: drive a locally-running Ollama model.

This keeps all traffic on localhost (http://127.0.0.1:11434 by default), in
line with the handout's LOCAL-evidence requirement. It uses only the Python
standard library so there is no extra dependency to install.

If the server is not running, generate() raises a clear error that the CLI
turns into a friendly message telling the user to run `ollama serve`.
"""

import json
import urllib.error
import urllib.request

from .base import Target


class OllamaTarget(Target):
    name = "ollama"

    def __init__(self, model: str = "llama3.2",
                 base_url: str = "http://127.0.0.1:11434",
                 timeout: int = 120):
        self.model = model
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.name = f"ollama:{model}"

    def generate(self, system: str, user: str) -> str:
        url = f"{self.base_url}/api/chat"
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system or ""},
                {"role": "user", "content": user or ""},
            ],
            "stream": False,
            # temperature 0 keeps runs reproducible, which matters for evidence.
            "options": {"temperature": 0},
        }
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            url, data=data, headers={"Content-Type": "application/json"}
        )
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                body = json.loads(resp.read().decode("utf-8"))
            return body.get("message", {}).get("content", "")
        except urllib.error.URLError as exc:
            raise RuntimeError(
                f"Could not reach Ollama at {self.base_url}. "
                f"Is it running? Try `ollama serve`. Original error: {exc}"
            ) from exc
