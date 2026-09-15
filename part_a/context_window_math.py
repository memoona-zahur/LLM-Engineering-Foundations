"""Week 07 Day 1 · Part A #2 — Context-window arithmetic.
Given window size + estimated tokens-per-message, how many turns exhaust the window?"""

def turns_until_exhaustion(window_tokens, user_msg_tokens, assistant_msg_tokens, system_prompt_tokens=0):
    """Turns = one user + one assistant message. Returns (max_full_turns, tokens_remaining)."""
    per_turn = user_msg_tokens + assistant_msg_tokens
    usable = window_tokens - system_prompt_tokens
    full_turns = usable // per_turn
    remaining = usable - (full_turns * per_turn)
    return full_turns, remaining

# Case 1: llama3.2:3b uses 4K context (Ollama default num_ctx=4096)
WINDOW_4K = 4096
# Real conversation estimate (chat-based, roughly 3 sentences each side)
USER_MSG = 50      # user message ~50 tokens
ASSIST_MSG = 150   # assistant reply ~150 tokens

t1_full, t1_remain = turns_until_exhaustion(WINDOW_4K, USER_MSG, ASSIST_MSG, 200)
print("=== CASE 1: 4K window (llama3.2:3b local default), system prompt 200 tokens ===")
print(f"  window=4096, per-turn={USER_MSG}+{ASSIST_MSG}=200, system=200")
print(f"  -> usable={4096-200}, max FULL turns = {t1_full} (then ~{t1_remain} tokens left)")
print(f"  So after ~{t1_full} back-and-forth turns the oldest part of the convo is dropped.")

print()
# Case 2: 8k window, longer messages (typical R1 deepseek local 8k context)
WINDOW_8K = 8192
USER_MSG2 = 120
ASSIST_MSG2 = 400
t2_full, t2_remain = turns_until_exhaustion(WINDOW_8K, USER_MSG2, ASSIST_MSG2, 500)
print("=== CASE 2: 8K window (deepseek-r1:8b), each side longer ===")
print(f"  window=8192, per-turn={USER_MSG2}+{ASSIST_MSG2}=520, system=500")
print(f"  -> usable={8192-500}, max FULL turns = {t2_full} (that leaves ~{t2_remain} tokens)")
print(f"  So ~{t2_full} exchanges in, the conversation history silently truncates.")

print()
print("=== INTERPRETATION ===")
print("'The model forgot what I said earlier' is almost always this truncation, not a")
print("memory bug in the model. The model has NO memory outside the current request;")
print("whatever sends the request drops older turns to fit the window.")
