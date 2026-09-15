# Week 07 · Day 1 — LLM Engineering Foundations

**Transformers, Tokens, Prompting, and Your First Local Model**

First day of the "AI-first engineering" week: understand what a transformer actually
does, tokenize real text, reason about context windows, apply the five core prompting
techniques, and run **two real open-weight models entirely on your own machine** — no
API key, no cloud.

## What's in this repo

| Item | Purpose |
|---|---|
| `day1_llm_foundations.ipynb` | **The main deliverable** — self-contained notebook/report (read the markdown alone to understand everything; the code cells produce the evidence) |
| `part_a/` | Kata A scripts: `tokenizer_exercise.py`, `context_window_math.py` |
| `part_b/` | Kata B scripts: `prompts_task3.py` (zero/few-shot), `prompts_task4.py` (CoT), `prompts_task_role.py` (role), `prompts_task_chain.py` (chaining) |
| `evidence/` | Captured live runs for every claim (+ `run_prompt.py`, a reusable Ollama runner) |
| `EVIDENCE_REPORT.md` | Task → evidence mapping for all 10 "Today's tasks" |
| `technical_summary.md` | Technical write-up (environment, approach, findings, limitations) |
| `self_review.md` | Self-review against the checklist before submission |
| `verify_project.py` | Final integrity check — `python3 verify_project.py` |
| `test_day1.py` | **"Markdown == live recompute" tests** — `python3 test_day1.py` |
| `requirements.txt` | Python deps (`tiktoken==0.14.0`, `jupyter`, `nbformat`) |

## Prerequisites — Ollama and the two models

The notebook talks **only** to your local Ollama server at `http://localhost:11434`.
There is **no hosted API, no API key, no network dependency** after the models are
downloaded. So before anything else, this must work:

```bash
ollama --version   # if this fails, Ollama is not installed
```

### Step 1 — Install Ollama (Linux)

```bash
sudo snap install ollama
ollama --version        # should print 0.33.x or newer
```

### Step 2 — Pull the two models (one-time download, ~7.2 GB total)

```bash
ollama pull llama3.2:3b       # 2.0 GB
ollama pull deepseek-r1:8b    # 5.2 GB
ollama list                   # both models must appear here
```

### Step 3 — Smoke-test each model before running the notebook

```bash
ollama run llama3.2:3b        # type a question, press Enter; exit with /bye
ollama run deepseek-r1:8b     # this one shows its own reasoning before the answer
```

### Step 4 — Confirm the server is up (do this right before the notebook)

```bash
curl -s http://localhost:11434/api/tags
# Should print JSON containing both model names. Empty/failing response
# means the server is down — restart it:
# sudo snap restart ollama
```

> **Common mistake #1:** opening the notebook while Ollama is stopped. The model
> cells will fail. Fix: start Ollama (`ollama serve` or `sudo snap restart ollama`),
> re-run `curl` above, then **Restart & Run All** again.
>
> **Common mistake #2:** skipping the pull. If you get
> `Error: pull model manifest: ... not found`, you pulled nothing — run
> `ollama pull` for both names exactly as written above.

## Quick start — Python environment

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

python3 test_day1.py              # "markdown == live recompute" tests (exit 0 = no drift)
python3 verify_project.py         # full integrity audit (structure + evidence + notebook + live models)
```

**What `test_day1.py` proves:** deterministic artifacts (tokenizer math, context-window
turn counts) are recomputed from the actual `part_a` sources and asserted *exactly*
against both the notebook cell outputs and the markdown claims — the zero-markdown-drift
guarantee. Model cells (llama/R1) are stateful, so they're checked *structurally*
(valid JSON, viable risk label) rather than byte-for-byte; the notebook's Reproducibility
notes explain this split explicitly.

## Run the notebook (two ways)

**Option A — in Jupyter:** `jupyter notebook day1_llm_foundations.ipynb`, then
**Kernel → Restart & Run All**.

**Option B — headless:**

```bash
python3 -m nbconvert --to notebook --execute --inplace \
  --ExecutePreprocessor.timeout=400 day1_llm_foundations.ipynb
```

Expected wall time ≈ 5–7 minutes (the two DeepSeek live cells dominate; the unbounded
R1 puzzle is quoted from evidence rather than re-run).

> **Common mistake #3:** stopping the run mid-way (especially during a DeepSeek cell).
> This can leave a zombie generation on the server that blocks every later model call.
> Fix: `sudo snap restart ollama`, then re-run. This is exactly why the notebook's T3
> cell quotes the R1 puzzle from evidence instead of re-running it live.

## The five headline findings

1. A token is not a word: 42 words ≈ 51 tokens; boundaries split compounds and even
   the hyphen out of `re-verified`.
2. A model's "forgetting" is a context-window arithmetic problem, not a memory bug:
   19 turns at 4K vs 14 turns at 8K for realistic messages.
3. Quantization (`Q4_K_M`) is why an 8.2B-parameter model (16 GB full-precision) runs in
   a 5.2 GB GGUF file on a laptop.
4. Asking for CoT makes reasoning *auditable*, not *correct* — the local Llama followed
   the steps but did the math wrong; R1 reasons unprompted and went deeper (noticing a
   genuine ambiguity) but over-analyzed and never settled on that same puzzle.
5. Few-shot/role/chaining all run on the local models and each shape output visibly —
   but the honest headline is that on a 3B model the biggest wins come from *format
   control* (JSON staying valid), not from upstream-model levels of reasoning.

## Environment

Ollama 0.33.3 (snap), Ubuntu, CPU-only, 31 GiB RAM. Models: `llama3.2:3b` (2.0 GB) and
`deepseek-r1:8b` (5.2 GB). No hosted API used anywhere in this repo.