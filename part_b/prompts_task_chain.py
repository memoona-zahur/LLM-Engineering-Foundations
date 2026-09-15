"""Week 07 Day 1 · Part B #3c — Prompt chaining for the SAME loan classification task.
Breaks one complex multi-part task into a sequence of smaller prompts; each prompt's
output feeds the next. Same 'single responsibility' instinct as small functions.

Step 1: extract the facts only (no judgment).
Step 2: classify based on the extracted facts (no re-reading the raw text)."""

# --- Step 1: extract facts only ---
STEP1_EXTRACT = """You are a data extraction assistant. Given an applicant description,
list ONLY the objective facts as bullet points. Do not comment, do not judge, do not
recommend anything.

Applicant: A civil engineer with 6 years tenure at the same firm, no defaults on record,
monthly income 3.4x the requested loan installment.

Facts:"""

# --- Step 2: classify based on step-1 facts ---
STEP2_CLASSIFY_BASE = """You are a credit risk classifier. Based solely on the facts below,
classify the loan as 'low_risk', 'medium_risk', or 'high_risk'. Answer in a fixed JSON
object exactly:
{"risk": "<level>", "reason": "<one short sentence>"}

Facts:
{facts}

Answer:"""

if __name__ == "__main__":
    print("=== STEP 1 PROMPT ===")
    print(STEP1_EXTRACT)
    print("\n=== STEP 2 PROMPT (template — facts injected after step 1 runs) ===")
    print(STEP2_CLASSIFY_BASE.format(facts="[step 1 output goes here]"))