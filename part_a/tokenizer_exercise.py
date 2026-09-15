"""Week 07 Day 1 · Part A #1 — Tokenizer exercise with OpenAI's cl100k_base tokenizer.
Task: tokenize 3-4 sentences of MY OWN writing (from my daily status update) and note surprises."""
import tiktoken

enc = tiktoken.get_encoding("cl100k_base")

my_writing = (
    "Completed an in-depth, concept-by-concept walkthrough of the ML Pipeline Practical: "
    "went through the entire pipeline one step at a time and for each step wrote down its "
    "core concept in a line and re-verified its actual numbers from a fresh live run."
)

tokens = enc.encode(my_writing)
words = my_writing.split()

print("=== INPUT TEXT ===")
print(my_writing)
print(f"\nCharacters: {len(my_writing)}")
print(f"Words: {len(words)}")
print(f"Tokens: {len(tokens)}")
print(f"Tokens per word (avg): {len(tokens)/len(words):.2f}")
print(f"Tokens per character (avg): {len(tokens)/len(my_writing):.3f}")

print("\n=== SURPRISING / INTERESTING TOKEN BOUNDARIES ===")
for i, (tok, chunks) in enumerate(zip(tokens, enc.decode_tokens_bytes(tokens))):
    display = chunks.decode("utf-8", errors="replace").replace("\n", "\\n")
    if " " not in display or len(display) > 1:
        print(f"  token#{i:02d} = {display!r}")

print("\n=== TOKENIZED VIEW (token boundaries shown) ===")
for chunk in enc.decode_tokens_bytes(tokens):
    print(f"[{chunk.decode('utf-8', errors='replace')}]", end=" ")
print()
