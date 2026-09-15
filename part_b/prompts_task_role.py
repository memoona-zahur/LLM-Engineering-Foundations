"""Week 07 Day 1 · Part B #3b — Role prompting for the SAME loan classification task.
Zero-shot/few-shot tasks were evaluated without a persona. Here we add an explicit
role to condition which training patterns the model draws on.

Role chosen deliberately: 'senior credit risk analyst' — domain-grounded, justifiable
for a banking-adjacent task, and a realistic production persona for this payload type.
'Why not X': a generic 'you are a helpful assistant' persona was rejected because it
adds nothing beyond the task instruction (no conditioning value)."""

ROLE_PROMPT = """You are a senior credit risk analyst at a Tier-1 bank with 20 years of
underwriting experience. Your judgment determines whether the bank accepts or rejects
a loan application, so you are careful, precise, and evidence-based in every assessment.
You calibrate your risk levels to real banking practice: repayment capacity, credit
history, and exposure relative to income drive your decision.

Read the applicant description and classify the loan as 'low_risk', 'medium_risk', or
'high_risk'. Answer in a fixed JSON object exactly:
{"risk": "<level>", "reason": "<one short sentence>"}

Applicant: A civil engineer with 6 years tenure at the same firm, no defaults on record,
monthly income 3.4x the requested loan installment.

Answer:"""

if __name__ == "__main__":
    print(ROLE_PROMPT)