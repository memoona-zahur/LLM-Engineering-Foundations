"""Reusable runner: sends a prompt to a local Ollama model via the HTTP API and
prints response + timing. Properly JSON-escapes newlines. Only sends `think`
for models that support thinking (checked via /api/tags capabilities)."""
import json
import sys
import urllib.request

MODEL = sys.argv[1]
PROMPT = sys.stdin.read()

TEMP = float(sys.argv[2]) if len(sys.argv) > 2 else 0.1

with urllib.request.urlopen("http://localhost:11434/api/tags", timeout=15) as resp:
    tags = json.load(resp)
caps = [m["capabilities"] for m in tags["models"] if m["name"] == MODEL]
supports_thinking = bool(caps and "thinking" in caps[0])

body = {
    "model": MODEL,
    "prompt": PROMPT,
    "stream": False,
    "options": {"temperature": TEMP},
}
if supports_thinking:
    body["think"] = True

req = urllib.request.Request(
    "http://localhost:11434/api/generate",
    data=json.dumps(body).encode(),
    headers={"Content-Type": "application/json"},
)
with urllib.request.urlopen(req, timeout=600) as resp:
    r = json.load(resp)

if r.get("thinking"):
    print("=== THINKING ===")
    print(r["thinking"])
    print()
print("=== RESPONSE ===")
print(r.get("response", r.get("error", "")))
print()
print(f"temperature: {TEMP}")
print(f"eval_count: {r.get('eval_count')}")
print(f"eval_duration_s: {round(r.get('eval_duration', 0) / 1e9, 2)}")
if r.get("error"):
    sys.exit(1)