# 🏁 Run, Screenshot & Submit Guide (do this on your laptop)

This is your step-by-step checklist to turn the repo into a complete A4
submission. Follow top to bottom. ⏱️ ~30–40 minutes total.

---

## ✅ Step 0 — What's already done for you

The repo is built, tested, and already produced working reports:
- `reports/mock_report.html` + `.json` (48 cases, 56.2% ASR)
- `docs/A4_findings_report.pdf` (the short findings PDF — deliverable #3)
- `screenshots/report_preview.png` (sample)

You still need to: **run it yourself, screenshot it, push to GitHub, record the video.**

---

## 🧰 Step 1 — Put the folder on your laptop

1. Download the `sentinel-ai` folder I gave you.
2. Open a terminal **inside** that folder. Verify:
   ```bash
   cd path/to/sentinel-ai
   python --version        # need 3.9+
   ```
   💡 If `python` fails, try `python3` everywhere below.

---

## 📸 Step 2 — Task 1 "LEARN": run every command & screenshot

Run these **one at a time** and screenshot each output. These are your
"mastering the features command by command" screenshots.

```bash
python -m sentinel --version
python -m sentinel list-strategies
python -m sentinel list-probes  -c configs/mock_canary.json
python -m sentinel validate     -c configs/mock_canary.json
python -m sentinel run -c configs/mock_canary.json \
    --json reports/mock_report.json --html reports/mock_report.html
```

Then open the report and screenshot it:
```bash
# Linux:
xdg-open reports/mock_report.html
# macOS:   open reports/mock_report.html
# Windows: start reports/mock_report.html
```
📷 **Screenshots to capture (save into `screenshots/`):**
1. `--version` + `list-strategies`
2. `list-probes`
3. `validate` (shows "total cases: 48")
4. `run` output (the FAIL/ok progress + Summary block)
5. The HTML report, top (summary cards + ASR tables)
6. The HTML report, one expanded evidence row (click a red "view")

---

## 🧪 Step 3 — show the tests pass

```bash
python tests/test_sentinel.py
```
📷 Screenshot the "4 tests passed." output.

---

## 🔁 Step 4 — show a config change (proves it's configurable)

Run just two strategies to show the override works:
```bash
python -m sentinel run -c configs/mock_canary.json \
    --strategies plain,base64 --repeat 1 \
    --json reports/quick.json --html reports/quick.html
```
📷 Screenshot — notice `total cases` and ASR change. Good talking point for the video.

---

## 🦙 Step 5 (OPTIONAL but impressive) — run against a real model

Only if you install Ollama. Skipping this is fine; the mock run is a complete submission.
```bash
# one-time:
#   install Ollama from https://ollama.com
ollama serve            # leave running in one terminal
ollama pull llama3.2    # in another terminal

pip install pyyaml      # to read the .yaml config
python -m sentinel run -c configs/ollama_canary.yaml --model llama3.2 \
    --json reports/llama_report.json --html reports/llama_report.html
```
📷 Screenshot the run + report. ⚠️ A real model may refuse more often than the
mock — that's a *genuine* and interesting result; report whatever you actually see.

---

## 🐙 Step 6 — push to GitHub

```bash
cd sentinel-ai
git init
git add .
git commit -m "Sentinel-AI: canary-token LLM guardrail red-teaming tool (A4)"
# make an empty repo on github.com first (name it sentinel-ai), then:
git remote add origin https://github.com/<your-username>/sentinel-ai.git
git branch -M main
git push -u origin main
```
✅ Open the repo page and confirm the README renders.

---

## 🎥 Step 7 — record the video

Use the script in `docs/VIDEO_SCRIPT.md`. ~4–6 minutes. Screen-record with:
- Windows: **Xbox Game Bar** (`Win + G`) or OBS
- macOS: **QuickTime** (File → New Screen Recording) or `Cmd+Shift+5`

---

## 📤 Step 8 — submit

Open the **A4 submission form** (QR / "Open A4 submission form" link in the handout) and attach:
1. ✅ Screenshots (Promptfoo/Garak-style command outputs — yours are Sentinel's) + the local reports
2. ✅ GitHub repository link
3. ✅ `docs/A4_findings_report.pdf`
4. ✅ The video

---

## 🧭 Honesty checklist (so you can defend it like an interview)

Before you submit, make sure you can answer these out loud:
- **Why a canary token instead of real harmful content?** → Same security signal (can the guardrail be broken?), zero hazardous output, safe to publish.
- **Why do base64/rot13 hit 100%?** → The keyword filter can't see banned words inside an encoded blob, so the request passes, then the model decodes and obeys.
- **Why is leetspeak 0%?** → It dodges the filter but the target never un-leets it, so the request is never acted on — shows filter coverage is uneven.
- **What's the fix?** → Decode/normalise before checking; enforce a trust boundary; add an output-side guard.
- **What would change with a real model?** → Numbers differ; the method is identical. That's the value of the `Target` interface.
