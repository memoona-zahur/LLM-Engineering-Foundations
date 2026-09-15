"""Week 07 Day 1 · Part B #3 — Zero-shot vs few-shot prompts for the SAME task.
Task: extract loan risk assessment from a short applicant description and output a
strict JSON object. Output format is the thing few-shot should improve."""

TASK = (
    "Read the applicant description and classify the loan as 'low_risk', "
    "medium_risk', or 'high_risk'. Answer in a fixed JSON object exactly:\n"
    '{"risk": "<level>", "reason": "<one short sentence>"}'
)

# ---- ZERO-SHOT: no examples ----
ZERO_SHOT = (
    TASK
    + "\n\nApplicant: A civil engineer with 6 years tenure at the same firm, "
    "no defaults on record, monthly income 3.4x the requested loan installment.\n\nAnswer:"
)

# ---- FEW-SHOT: 3 worked examples before the asked one ----
EXAMPLES = """Example 1:
Applicant: Freelance graphic designer, income varies month to month, has one 60-day-late payment last year.
Answer: {"risk": "high_risk", "reason": "variable income and a recent late payment signal repayment unpredictability"}

Example 2:
Applicant: Teacher with 5 years at a stable school, clean credit file, borrowing one-third of annual salary.
Answer: {"risk": "low_risk", "reason": "stable employer, clean record, and a small loan relative to income"}

Example 3:
Applicant: Recent college graduate in first job, stable salary, small existing credit card debt, no defaults.
Answer: {"risk": "medium_risk", "reason": "stable-but-short work history with modest existing debt"}

"""

FEW_SHOT = (
    "Classify each applicant the same way. Use this exact format:\n"
    '{"risk": "<low_risk|medium_risk|high_risk>", "reason": "<one short sentence>"}\n\n'
    + EXAMPLES
    + "Applicant: A civil engineer with 6 years tenure at the same firm, no defaults on "
    "record, monthly income 3.4x the requested loan installment.\nAnswer:"
)

if __name__ == "__main__":
    print("=== ZERO-SHOT PROMPT ===")
    print(ZERO_SHOT)
    print("\n" + "=" * 50)
    print("=== FEW-SHOT PROMPT ===")
    print(FEW_SHOT)