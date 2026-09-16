# Technical Summary — Week 07 Day 1: LLM Engineering Foundations

## 1. Objective

Bring "how a language model actually works" from a vague mental model to something
verified on my own machine. The day's three kata parts were: (A) tokens and context
windows, (B) the five core prompting techniques, (C) two real open-weight models
installed, pulled, and verified locally — **no hosted API, no API key, no network
dependency after download**.

The deliverable is a self-contained notebook (`day1_llm_foundations.ipynb`) that reads
as a report, with every live model run captured as evidence files and audited by
`verify_project.py`.

## 2. Environment & Tools

| Item | Value |
|---|---|
| Machine | Dell Latitude 5590, Ubuntu, CPU-only (Intel UHD 620) |
| RAM | 31 GiB total (models loaded cleanly, no swap used) |
| Python | 3.10.12 |
| Ollama | 0.33.3 (snap package), server at `localhost:11434` |
| Tokenizer | `tiktoken` 0.14.0, `cl100k_base` (GPT-4-class encoding) |
| Models (live) | `llama3.2:3b` (Q4_K_M, 3.2B, 2.0 GB) · `deepseek-r1:8b` (Q4_K_M, 8.2B, 5.2 GB) |

## 3. Approach

Everything was run against **real, local artifacts** and captured to files — no figures
quoted from memory. The notebook embeds the same logic inline (self-contained, runs
anywhere), while `part_a/` and `part_b/` hold the standalone kata scripts. Evidence
files in `evidence/` record the exact runs that the report quotes; `verify_project.py`
re-checks structure, key numbers, notebook health, and live model availability.

## 4. Findings

### Part A — concepts made concrete
- **Tokens:** 42 words of my own writing = **51 tokens** (1.21 tokens/word, ~0.2/char).
  Boundaries are non-obvious: `concept-by-concept` splits as `[-by][-con][cept]`;
  `re-verified` becomes `[re][-][verified]` (hyphen is its own token).
- **Context windows:** 4K window with short messages → **19 full turns**; 8K window with
  longer messages → **14 full turns**. The model "forgets" because the caller drops old
  tokens to fit the window — not because the model's memory fades.
- **Quantization:** Q4 (4-bit) GGUF files let 3.2B and 8.2B models run in RAM that could
  never hold their ~6–16 GB full-precision weights; the exact tag is `Q4_K_M`
  (4-bit K-quantization, medium variant — K is the llama.cpp K-quant scheme family,
  not k-means; M keeps a few sensitive tensors at higher precision).

### Part B — prompting techniques (all applied to the same loan-classification task)
| Technique | Live result (llama3.2:3b) |
|---|---|
| Zero-shot | Valid JSON, `low_risk` |
| Few-shot (3 ex) | Valid JSON, `low_risk`, slightly richer reason |
| Chain-of-thought | Reasoning visible → auditable, but math wrong (months vs years) |
| Role prompting | Persona-calibrated, JSON kept, domain-grounded reason |
| Prompt chaining | Step 1 pure facts → Step 2 clean JSON classification |
| Temperature | 0.0 deterministic · 0.8 coherent/varied · 1.5 coherence breaks |

Chosen policy for all evidence runs: **temperature 0.1** (deterministic tasks).

### Part C — two local models verified
- **llama3.2:3b** answered the bank-credit question correctly (creditworthiness, income
  stability, debt load), ~10.5 tokens/s on CPU.
- **deepseek-r1:8b** (thinking-capable) produced its own visible reasoning *before* the
  answer, unprompted, ~3.9 tokens/s.
- **Core insight (Kata #9, two sentences):** a model that reasons because you asked it to
  (Llama CoT) follows the step structure and settles — auditable, but it can still be
  wrong; a model that reasons because it was trained to (DeepSeek-R1) goes deeper
  unprompted, catching nuances the simpler model misses, but that same depth can turn
  into over-analysis — on the ambiguous-interest puzzle R1 never settled within
  10+ minutes.

### Honest limitations documented
- Local 3B/8B models can give plausible-but-wrong answers; we verified *real* output,
  not perfect correctness.
- Prompt comparisons were single runs (temp 0.1), not replicated — no sampling-variance
  estimates.
- CPU-only; token/s figures would improve with a discrete GPU.
- R1's never-settling on one puzzle is documented as a model+task limitation, not hidden.
- Context-window arithmetic uses token-size estimates, not measured conversation counts.

## 5. Verification (`python3 verify_project.py`)

Checks: all 9 required files exist, all 15 evidence files present and non-empty,
key numbers match evidence (51 tokens, 19/14 turns), notebook executes with zero error
cells, tiktoken pinned in requirements, both models registered live in Ollama.
Status after final notebook run: **ALL CHECKS PASSED**.

## 6. Reproducibility

- `requirements.txt` pins `tiktoken==0.14.0`, `jupyter`, `nbformat`.
- Predictable parts (tokenizer math) are deterministic; model outputs are stateful and
  vary slightly run-to-run — pinned by model name + `Q4_K_M` + temperature 0.1, with
  evidence files capturing the exact quoted runs.
- Restart & Run All: expected wall time ≈ 5–7 minutes (the two R1 live cells dominate;
  the unbounded R1 puzzle is quoted from evidence instead of re-run).