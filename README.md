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
| `requirements.txt` | Python deps (`tiktoken==0.14.0`, `jupyter`, `nbformat`) |

## Quick start

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

python3 verify_project.py          # integrity audit (exit 0 = all pass)
ollama --version                   # needs Ollama 0.33+ running locally
```

To re-run the notebook:

```bash
python3 -m nbconvert --to notebook --execute --inplace \
  --ExecutePreprocessor.timeout=400 day1_llm_foundations.ipynb
```

Expected wall time ≈ 5–7 minutes (the two DeepSeek live cells dominate; the unbounded
R1 puzzle is quoted from evidence rather than re-run).

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