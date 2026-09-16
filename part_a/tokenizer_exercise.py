"""Week 07 Day 1 · Part A #1 — Tokenizer exercise with OpenAI's cl100k_base tokenizer.
Task: tokenize 3-4 sentences of MY OWN writing (from my daily status update) and note surprises."""
import tiktoken

enc = tiktoken.get_encoding("cl100k_base")

MY_WRITING = (
    "Completed an in-depth, concept-by-concept walkthrough of the ML Pipeline Practical: "
    "went through the entire pipeline one step at a time and for each step wrote down its "
    "core concept in a line and re-verified its actual numbers from a fresh live run."
)

TOKENS = enc.encode(MY_WRITING)
WORDS = MY_WRITING.split()

print("=== INPUT TEXT ===")
print(MY_WRITING)
print(f"\nCharacters: {len(MY_WRITING)}")
print(f"Words: {len(WORDS)}")
print(f"Tokens: {len(TOKENS)}")
print(f"Tokens per word (avg): {len(TOKENS)/len(WORDS):.2f}")
print(f"Tokens per character (avg): {len(TOKENS)/len(MY_WRITING):.3f}")

print("\n=== SURPRISING / INTERESTING TOKEN BOUNDARIES ===")
for i, (tok, chunks) in enumerate(zip(TOKENS, enc.decode_tokens_bytes(TOKENS))):
    display = chunks.decode("utf-8", errors="replace").replace("\n", "\\n")
    if " " not in display or len(display) > 1:
        print(f"  token#{i:02d} = {display!r}")

print("\n=== TOKENIZED VIEW (token boundaries shown) ===")
for chunk in enc.decode_tokens_bytes(TOKENS):
    print(f"[{chunk.decode('utf-8', errors='replace')}]", end=" ")
print()
