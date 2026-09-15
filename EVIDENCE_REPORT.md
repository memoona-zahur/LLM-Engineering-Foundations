# Week 07 · Day 1 — Evidence Report
## LLM Engineering Foundations: Transformers, Tokens, Prompting, and First Local Model

**Date:** 2026-09-15 | **Machine:** Latitude 5590, 31 GiB RAM, CPU-only, Ubuntu

---

## Part A — Concepts Made Concrete

### A1. Tokenizer Exercise
- **Input:** 42-word sentence from own writing
- **Result:** 51 tokens (1.21 tokens/word, 0.205 tokens/char) — `tiktoken` cl100k_base
- **Surprises:** `concept` split as `[-by][-con][cept]` (unexpected multi-chunk split); `re-verified` → `re[-]verified` (hyphen creates separate token); `Pipeline` and `Practical` stay whole (common training words)
- **Evidence file:** `evidence/partA1_tokenizer.txt`

### A2. Context-Window Arithmetic
- 4K window + short msgs → **19 full turns** before oldest content truncated
- 8K window + longer msgs → **14 full turns** before truncation
- **Key insight:** "the model forgot" = truncation, not a memory bug. The model has NO memory outside the current request text.
- **Evidence file:** `evidence/partA2_context_window.txt`

---

## Part B — Prompts Planned (Ready for Testing)

### B3. Zero-shot vs Few-shot Prompts
- **Task:** Loan risk classification → strict JSON output
- **Zero-shot:** instruction only, no examples
- **Few-shot:** 3 worked examples (high/low/medium risk) before the target query
- **Files:** `part_b/prompts_task3.py`

### B4. Chain-of-Thought Comparison
- **Task:** Compare two loan offers (flat annual rates, different terms)
- **Without CoT:** "Show only the final answer"
- **With CoT:** "Think step by step: compute interest 1, total 1, interest 2, total 2, compare"
- **Reference correct answer:** Offer 1 = $11,200 total (lower than Offer 2's $11,350)
- **Files:** `part_b/prompts_task4.py`

---

## Part C — Deploy and Verify Two Real Local Models

### C5. Ollama Installed
- Version: 0.33.3 (via snap)
- Server running at `127.0.0.1:11434`

### C6. llama3.2:3b Verified ✅
- Pulled: 2.0 GB, Q4_K_M quantization, 3.2B params
- First question: "3 things a bank should check before approving a loan"
- Answer: Coherent, correct (creditworthiness, income stability, debt-to-income)
- Speed: ~10.5 tokens/sec (CPU-only), acceptable for interactive use
- **Evidence file:** `evidence/partC_llama3_real_question.txt`

### C7. deepseek-r1:8b Verified ✅
- Pulled: 5.2 GB, Q4_K_M quantization, 8.2B params, reasoning model
- First question: same loan question
- **Visible unprompted reasoning** produced before answer (training-based, not prompted)
- Reasoning included: assessing repayment ability, credit history, loan purpose
- Answer: coherent, correct, all three factors well-defined
- Speed: ~3.9 tokens/sec (CPU-only); with thinking, 10+ minutes for complex queries
- **Evidence file:** `evidence/partC_deepseek_r1_thinking.txt`

### C8. Few-shot vs Zero-shot Test on Local Model
- **Zero-shot result:** `{"risk":"low_risk","reason":"stable income and no credit history issues"}`
- **Few-shot result:** `{"risk":"low_risk","reason":"stable employment, clean record, and a high income relative to loan installment"}`
- **Honest note:** Both produced valid JSON, same classification. Few-shot gave a slightly more specific reason, but zero-shot also worked fine for this case. llama3.2:3b is format-robust enough that zero-shot alone produced correct JSON for this task.
- **Evidence file:** `evidence/partC_zeroshot_vs_fewshot_llama.txt`

### C9. CoT Comparison — Key Finding

**Llama3.2:3b (prompted reasoning):**
- NO-CoT: Said "Offer 2" — **WRONG** (correct is Offer 1)
- WITH-CoT: Showed steps but calculated interest as $10,000 × 0.06 × 24 = $14,400 (confused months with years in flat-rate formula). Reached a conclusion but wrong math

**DeepSeek-R1:8b (unprompted reasoning):**
- Correctly began computing Offer 1 interest = $1,200
- Then detected ambiguity in "flat rate" terminology for Offer 2 (which doesn't specify monthly installments)
- **Got stuck in analysis loop** — 10+ minutes, never produced a final answer
- The model was reasoning correctly about genuine ambiguity but over-analyzed

**Two-sentence contrast:**
> "A model that reasons because you asked it to (Llama CoT) follows the requested step structure mechanically and reaches an answer, even if wrong. A model that reasons because that's how it was trained (R1) detects genuine hidden complexity that simpler models miss, but can get stuck over-analyzing rather than reaching a conclusion."

- **Evidence file:** `evidence/part9_cot_contrast_analysis.txt`, `evidence/partC_cot_comparison_llama.txt`

### C10. Resource Usage
- Total disk: 6.8 GB (both models + runtime)
- llama3.2:3b: ~10.5 tokens/sec, tolerable chat experience
- deepseek-r1:8b with thinking: ~3.9 tokens/sec, can take 10+ min on complex queries
- Both load into RAM cleanly, no swap, no crash
- **Evidence file:** `evidence/part10_resource_usage.txt`

---

## Completion Checklist (from spec)

| Task | Status | Evidence |
|------|--------|----------|
| Tokenizer exercise, surprising boundaries noted | ✅ | `partA1_tokenizer.txt` |
| Context-window arithmetic done | ✅ | `partA2_context_window.txt` |
| Zero-shot and few-shot prompts written for same task | ✅ | `part_b/prompts_task3.py` |
| CoT comparison prompts written | ✅ | `part_b/prompts_task4.py` |
| Ollama installed and confirmed running | ✅ | `ollama --version` output |
| Llama model pulled, run, verified with real answer | ✅ | `partC_llama3_real_question.txt` |
| Chinese open-weight model pulled, run, verified | ✅ | `partC_deepseek_r1_thinking.txt` |
| Few-shot tested against local model, difference noted | ✅ | `partC_zeroshot_vs_fewshot_llama.txt` + honest note |
| CoT comparison run on R1, unprompted vs prompted contrasted | ✅ | `part9_cot_contrast_analysis.txt` |
| Resource usage impression noted | ✅ | `part10_resource_usage.txt` |
