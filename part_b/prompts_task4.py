"""Week 07 Day 1 · Part B #4 — Chain-of-thought comparison prompts.
Same multi-step reasoning task, two versions:
  1. WITHOUT step-by-step requested  (answer directly)
  2. WITH explicit step-by-step asked (chain-of-thought)
Will be tested against llama3.2:3b (prompted reasoning) and DeepSeek-R1 (unprompted)."""

NO_COT = (
    "A bank offers a loan of $10,000 at a flat annual interest rate of 6% for 2 years, "
    "to be repaid in 24 equal monthly installments. A second offer is $10,000 at 4.5% for "
    "3 years. Which offer has the LOWER total amount repaid? Show only the final answer "
    "(name the lower offer)."
)

WITH_COT = (
    "A bank offers a loan of $10,000 at a flat annual interest rate of 6% for 2 years, "
    "to be repaid in 24 equal monthly installments. A second offer is $10,000 at 4.5% for "
    "3 years. Which offer has the LOWER total amount repaid? Think step by step: "
    "1) compute total interest of offer 1, 2) add principal for offer 1 total, "
    "3) compute total interest of offer 2, 4) add principal for offer 2 total, "
    "5) compare the two totals and state which is lower."
)

if __name__ == "__main__":
    print("=== NO-CoT PROMPT (answer only) ===")
    print(NO_COT)
    print("\n" + "=" * 50)
    print("=== WITH-CoT PROMPT (ask step-by-step) ===")
    print(WITH_COT)