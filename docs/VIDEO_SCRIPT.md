# 🎥 Video Script — Sentinel-AI (≈ 5 minutes)

The instructor said to treat this like a technical interview: explain your
work, show it running, prove you understand it. Speak in your own words — this
is a guide, not a teleprompter. Have the repo open in an editor + a terminal.

---

## 0:00 — Intro (20s)
> "Hi, I'm [name], a Computer Science–Cybersecurity student at PSU. For the A4
> capstone I built **Sentinel-AI**, a small red-teaming tool that measures how
> easily an LLM's safety guardrails can be defeated by prompt injection and
> encoding attacks — inspired by Promptfoo and Garak."

## 0:20 — The key design choice (40s) ⭐ most important part
> "A guardrail test should prove the model *refuses* bad requests. Instead of
> generating actually dangerous content to grade — which I didn't want in a
> public repo — I used a **canary-token** method. I plant a harmless secret in
> the system prompt and tell the model never to reveal it. An attack 'succeeds'
> only when the model leaks that harmless token. Same security signal, zero
> hazardous output. That's a deliberate, defensible engineering decision."

## 1:00 — Architecture tour (60s)
Open the folders as you talk:
> "It's modular — each concern in one folder: `targets` is what we send prompts
> to, a mock or a local Ollama model; `probes` holds the attack inputs and the
> encoding strategies — plain, base64, rot13, leetspeak; `detectors` decide if a
> single response leaked the canary; `evaluators` run every probe × strategy ×
> repetition and compute the Attack Success Rate; `reporting` writes the JSON and
> HTML evidence. The evaluator is written against a `Target` interface, so the
> same code drives the mock or a real model — I just change one flag."

## 2:00 — Run it live (90s)
Type each command, let output show:
```
python -m sentinel list-strategies
python -m sentinel validate -c configs/mock_canary.json
python -m sentinel run -c configs/mock_canary.json \
    --json reports/mock_report.json --html reports/mock_report.html
```
> "Validate shows 48 test cases. Now I run it… you can see each case marked ok or
> FAIL-leak in real time, and the summary: overall ASR 56%."

Open `reports/mock_report.html`:
> "Here's the evidence report — summary cards, ASR by category and by strategy,
> and a full log where every row has the exact attack input, the model's full
> response, and the verdict, so any finding is reproducible."

## 3:30 — Explain the results = understanding (60s)
Point at the strategy table:
> "The story is right here. **Base64 and ROT13 hit 100%** — the keyword filter
> only sees an encoded blob, so the banned words aren't visible, the request
> passes, and the model decodes and obeys. **Plain text is only 25%** because the
> filter catches the obvious keywords. **Leetspeak is 0%** — it dodges the filter
> but this target never un-leets it, which shows filter coverage is uneven.
> **Prompt injection is 75%** — fake 'admin override' text crosses a weak trust
> boundary. Root cause: keyword filtering gives false confidence; you must decode
> intent and enforce a trust boundary."

## 4:30 — Tests + extensibility (30s)
```
python tests/test_sentinel.py
```
> "Four automated regression tests lock in the behaviour. Adding a new attack
> strategy is one function; a new probe is one line of config; a new target is
> one file. It's built to be extended, like a real open-source tool."

## 5:00 — Close (15s)
> "So Sentinel-AI shows, with reproducible local evidence, that simple keyword
> guardrails fail against trivial encoding — and it does it safely. Thanks."

---

### 🎙️ Tips
- Show your **face or at least your voice** — they want to know *you* understand it.
- If you installed Ollama, add a 30s clip running `--model llama3.2` and note the
  numbers differ for a real model — that honesty scores well.
- Don't read code line-by-line; explain *why*, not *what*.
