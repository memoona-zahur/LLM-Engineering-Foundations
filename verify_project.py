"""verify_project.py — final integrity check for the Week 07 Day 1 project.

Run: python3 verify_project.py  (exit 0 = all checks pass)

Checks the same way the ML Pipeline project tested-a-sample/full: file structure,
key evidence numbers, notebook health, and live model availability.
"""
import json
import os
import sys
import urllib.request

ROOT = os.path.dirname(os.path.abspath(__file__))

FAILURES = []


def check(cond, msg):
    tag = "PASS" if cond else "FAIL"
    print(f"[{tag}] {msg}")
    if not cond:
        FAILURES.append(msg)


def path(*parts):
    return os.path.join(ROOT, *parts)


# 1. Required structure -----------------------------------------------------
REQUIRED_FILES = [
    "day1_llm_foundations.ipynb",
    "EVIDENCE_REPORT.md",
    "requirements.txt",
    "part_a/tokenizer_exercise.py",
    "part_a/context_window_math.py",
    "part_b/prompts_task3.py",
    "part_b/prompts_task4.py",
    "part_b/prompts_task_role.py",
    "part_b/prompts_task_chain.py",
]

print("== Structure ==")
for f in REQUIRED_FILES:
    check(os.path.isfile(path(f)), f"file exists: {f}")

# 2. Evidence files ---------------------------------------------------------
EXPECTED_EVIDENCE = [
    "partA1_tokenizer.txt",
    "partA2_context_window.txt",
    "partC_llama3_real_question.txt",
    "partC_deepseek_r1_thinking.txt",
    "partC_deepseek_r1_real_question.txt",
    "partC_zeroshot_vs_fewshot_llama.txt",
    "partC_cot_comparison_llama.txt",
    "partC_cot_comparison_r1.txt",
    "partC_r1_nocot.txt",
    "partC_r1_nocot_full.txt",
    "part9_cot_contrast_analysis.txt",
    "part_role_prompting.txt",
    "part_prompt_chaining.txt",
    "part_temperature_comparison.txt",
    "part10_resource_usage.txt",
]

print("\n== Evidence ==")
for f in EXPECTED_EVIDENCE:
    check(os.path.isfile(path("evidence", f)), f"evidence present: {f}")
    if os.path.isfile(path("evidence", f)):
        size = os.path.getsize(path("evidence", f))
        check(size >= 60, f"evidence non-empty ({size} bytes): {f}")

# 3. Key numbers inside the evidence ---------------------------------------
print("\n== Key evidence numbers ==")
tok = open(path("evidence", "partA1_tokenizer.txt"), encoding="utf-8").read()
check("Tokens: 51" in tok, "tokenizer: 42 words -> 51 tokens")
check("1.21" in tok, "tokenizer: 1.21 tokens/word")

ctx = open(path("evidence", "partA2_context_window.txt"), encoding="utf-8").read()
check("19" in ctx and "14" in ctx, "context window: 19 vs 14 full turns")

agent = open(path("evidence", "part_role_prompting.txt"), encoding="utf-8").read()
check("low_risk" in agent, "role prompting: classification present")

chain = open(path("evidence", "part_prompt_chaining.txt"), encoding="utf-8").read()
check("STEP 1" in chain and "STEP 2" in chain, "prompt chaining: both steps present")

temp = open(path("evidence", "part_temperature_comparison.txt"), encoding="utf-8").read()
check("temperature=" in temp.lower() or "temperature:" in temp.lower(),
      "temperature comparison captured")

# 4. Notebook health --------------------------------------------------------
print("\n== Notebook ==")
import nbformat  # noqa: E402
nb = nbformat.read(path("day1_llm_foundations.ipynb"), as_version=4)
code_cells = [c for c in nb.cells if c.cell_type == "code"]
check(len(code_cells) >= 12, f"notebook has >=12 code cells ({len(code_cells)})")
with_outputs = sum(1 for c in code_cells if c.get("outputs"))
check(with_outputs == len(code_cells), f"all code cells have outputs ({with_outputs}/{len(code_cells)})")
error_outputs = [
    c for c in code_cells
    if any(o.get("output_type") == "error" for o in c.get("outputs", []))
]
check(not error_outputs, f"no error cells in notebook ({len(error_outputs)} error cells)")

full_source = "\n".join(c.source for c in nb.cells if c.cell_type == "code")
all_source = "\n".join(c.source for c in nb.cells)
for section in ["T1", "T2", "T3", "T4", "T5"]:
    check(section in all_source, f"notebook (markdown+code) references {section}")
for section in ["llama3.2:3b", "deepseek-r1:8b"]:
    check(section in full_source, f"notebook code references {section}")

# 5. Requirements -----------------------------------------------------------
print("\n== Requirements ==")
req = open(path("requirements.txt"), encoding="utf-8").read()
check("tiktoken==0.14.0" in req, "tiktoken pinned in requirements.txt")
check("jupyter" in req, "jupyter in requirements.txt")

# 6. Live model availability ------------------------------------------------
print("\n== Ollama live ==")
try:
    with urllib.request.urlopen("http://localhost:11434/api/tags", timeout=10) as resp:
        tags = json.load(resp)["models"]
    names = {m["name"] for m in tags}
    check("llama3.2:3b" in names, "ollama: llama3.2:3b available")
    check("deepseek-r1:8b" in names, "ollama: deepseek-r1:8b available")
except Exception as exc:
    check(False, f"ollama reachable: {exc}")

print("\n" + ("ALL CHECKS PASSED" if not FAILURES else f"{len(FAILURES)} CHECK(S) FAILED"))
sys.exit(0 if not FAILURES else 1)