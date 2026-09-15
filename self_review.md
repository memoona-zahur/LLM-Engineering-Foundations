# Self-Review — Week 07 Day 1: LLM Engineering Foundations

*Self-review done before submission, mirroring the method used on the ML Pipeline
project (own-checks discipline).*

## Checklist

### 1. Done on time, tracked
- [x] All 10 "Today's tasks" items are complete and mapped to evidence
      (`EVIDENCE_REPORT.md`).
- [x] Daily status update form drafted (detail + summary + technical deep point).

### 2. Real working code, no stone left unturned
- [x] Every Part A/B/C item has a real, captured run — no placeholder claims.
- [x] Models are genuinely installed and verified live
      (`ollama --version` → 0.33.3; both models in `/api/tags`; real Q&A captured).
- [x] The notebook's model cells re-run live; evidence files are byte-stable
      records of the actual runs.

### 3. Written reasoning — not just "yes I did it"
- [x] Each finding has a plain-English explanation (why 51 tokens ≠ 42 words,
      why a model "forgets", why R1's thinking is different from CoT).
- [x] Two-sentence CoT-vs-R1 contrast written and saved separately.
- [x] Limitations are written up explicitly (not hidden)
      — that includes R1 never settling on one puzzle.

### 4. Honest comparison
- [x] Zero-shot vs few-shot noted honestly: on this local model few-shot's advantage
      was modest (richer reason, not better format validity).
- [x] CoT comparison notes the wrong math (months vs years) instead of claiming success.

### 5. Beyond minimum
- [x] Added transformer-in-plain-English (A0) — the conceptual foundation the spec's
      lessons cover.
- [x] Added quantization explanation (A3) — why local models fit in laptop RAM at all.
- [x] Added two additional techniques beyond the core kata: role prompting (B3) and
      prompt chaining (B4), both tested live.
- [x] Added generation-parameters demo (B5): temperature 0.0/0.8/1.5 on the same prompt.
- [x] `verify_project.py` — automated integrity audit of the whole deliverables folder.

### 6. Upward trajectory
- [x] Follows the exact structure that earned 9.7/10 on the ML Pipeline practical
      (notebook-as-report + evidence + verify + summary), now executed under the
      daily-task template.

## Cross-check of the three claimed gaps vs this project
| Earlier gap (from the professor's practice) | Where addressed today |
|---|---|
| Explain concepts in your own words | A0 transformer, A1 token boundaries, A2 window arithmetic, A3 quantization |
| Show you verified numbers by re-running | every evidence file is a fresh live run; verify_project.py re-checks |
| Practice good documentation & project structure | notebook report + technical_summary + evidence + verify script |

## What I would improve next time
- Replicate each prompt comparison 5× to quantify sampling variance (today: single runs
  at temp 0.1).
- Benchmark GPU offload vs CPU for the 8B model.
- Stream live token output in the notebook instead of capturing post-hoc text.