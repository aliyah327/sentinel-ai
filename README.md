# Sentinel-AI 🛡️

**A small, auditable red-teaming harness for LLM guardrails.**
Inspired by [Promptfoo](https://www.promptfoo.dev/) and [Garak](https://reference.garak.ai/), built for the ASCL AI Security Training (Prince Sultan University), Assignment A4.

Sentinel-AI measures how easily a chat model's guardrails can be defeated by
prompt-injection and encoding attacks — **without ever generating harmful
content.** It does this with a *canary-token* design: a secret string is
planted in the system prompt and the model is told never to reveal it. An
attack "succeeds" only when the model leaks that harmless token.

---

## Why this design (and why not a synthesis grader) 🧠

A guardrail test should prove the model *refuses* disallowed behaviour. The
cleanest, safest way to do that is a canary: the "disallowed behaviour" is
leaking a fake secret we planted ourselves. We get the exact same red-team
skills — prompt injection, encoding strategies (Base64 / ROT13 / leetspeak),
refusal detection, and attack-success-rate scoring — with **zero hazardous
output**, so the repo is safe to publish and reuse. That's what a real
security team would accept in their CI.

---

## Architecture 🏗️

Each concern lives in exactly one folder, so the tool is easy to read, test
and extend:

```
sentinel/
├── targets/      what we send prompts to   (mock  |  local Ollama)
├── probes/       attack inputs + strategies (plain/base64/rot13/leetspeak)
├── detectors/    decide if ONE response failed (canary leak, refusal)
├── evaluators/   run probes × strategies × repeats, compute ASR
├── reporting/    write JSON + self-contained HTML evidence
├── config.py     load YAML/JSON, apply CLI overrides
└── cli.py        the `sentinel` command
```

**Data flow:**

```
config ─▶ Target ─▶ Evaluator ──(for each probe × strategy × repeat)──▶ Detectors ─▶ RunResult ─▶ JSON + HTML
```

| Term (training) | Here |
|---|---|
| Target / provider | `targets/` (mock or `ollama:llama3.2`) |
| Probe | base attack in `probes/library.py` |
| Strategy / buff | transform in `probes/strategies.py` |
| Detector | `detectors/` (canary leak = pass/fail) |
| Attack Success Rate | `successes / attempts`, in `evaluators/engine.py` |
| Regression test | `tests/test_sentinel.py` |

---

## Install ⚙️

No third-party packages are required to run against the mock target.
Python 3.9+ only.

```bash
git clone <your-repo-url> sentinel-ai
cd sentinel-ai
# Optional, only to read .yaml configs instead of .json:
pip install pyyaml
```

---

## Quick start (no model needed) 🚀

```bash
# 1) See everything the tool can do
python -m sentinel --version
python -m sentinel list-strategies
python -m sentinel list-probes  -c configs/mock_canary.json

# 2) Validate a config (counts the test cases before running)
python -m sentinel validate     -c configs/mock_canary.json

# 3) Run the full benchmark and write reports
python -m sentinel run -c configs/mock_canary.json \
    --json reports/mock_report.json \
    --html reports/mock_report.html

# 4) Open the HTML evidence file
xdg-open reports/mock_report.html     # Linux
# open reports/mock_report.html       # macOS
# start reports/mock_report.html      # Windows
```

> Use `configs/mock_canary.yaml` instead if you installed PyYAML.

---

## Run against a real local model (Ollama) 🦙

All traffic stays on `localhost:11434`, so evidence remains **local**.

```bash
ollama serve                 # in one terminal
ollama pull llama3.2         # once

python -m sentinel run -c configs/ollama_canary.yaml \
    --model llama3.2 \
    --json reports/llama_report.json \
    --html reports/llama_report.html
```

The evaluator code is identical — only the target changes. That's the point
of the `Target` interface.

---

## Expected output 📊

Against the built-in mock, you should see roughly:

| Strategy | ASR | Reading |
|---|---|---|
| `plain` | ~25% | direct asks are mostly refused |
| `base64` | **100%** | encoding defeats the keyword filter |
| `rot13` | **100%** | same bypass |
| `leetspeak` | 0% | filter still catches this shape |

**Overall ASR ≈ 56%.** The lesson: a keyword-based guardrail gives a false
sense of safety — encoded inputs walk straight past it.

---

## Extending the tool 🔧

- **Add a strategy:** write one `str -> str` function in
  `probes/strategies.py` and add it to the `STRATEGIES` dict. Done.
- **Add a probe:** add a dict to `BUILTIN_PROBES`, or put `extra_probes:` in
  your config — no code change.
- **Add a target:** implement `generate(system, user)` in a new file under
  `targets/` and register it in `build_target()`.
- **Add a detector:** implement `check(response)` and register it in
  `detectors/build_detector()`.

---

## Testing ✅

```bash
python tests/test_sentinel.py       # plain stdlib
# or, if you have pytest:
python -m pytest -q
```

The tests lock in the core guarantees: strategies transform text, the
detector only flags real leaks, the mock refuses plain asks but leaks on
injection, and a full run yields a valid ASR.

---

## Repository layout 📁

```
sentinel-ai/
├── sentinel/           # the package (source)
├── configs/            # reusable YAML/JSON configs
├── tests/              # automated regression tests
├── reports/            # generated evidence (JSON + HTML)
├── docs/               # findings report + run guide
├── screenshots/        # evidence screenshots for submission
└── README.md
```

## Safety & scope 🔏

Sentinel-AI only re-encodes its own harmless request ("reveal the canary").
It does not generate, grade, or store instructions for weapons, drugs, or any
hazardous process. It is a guardrail-robustness tool, not a content
generator.

## License

MIT — free to clone, install, and reuse.

## Author

Built for ASCL AI Security Training, Prince Sultan University.
