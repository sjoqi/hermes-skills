#!/usr/bin/env python3
"""Head-to-head benchmark harness — copy and adapt.

Usage:
  source ~/.hermes/.env   (in the shell; keys are read from env, never printed)
  python3 head_to_head_harness.py [model_name]

Reads questions.json: {"system_prompt": "...", "questions": [{"id": 1, "category": "math", "question": "..."}]}
Calls each configured model with IDENTICAL params, saves raw JSON to
raw-test/<model>_q<id>.json, retries ONCE on error. Cache-aware: skips existing files.
"""
import json, os, sys, time, urllib.request, urllib.error

BASE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(BASE, "raw-test")
os.makedirs(RAW, exist_ok=True)

# --- ADAPT: per-model config. Keys come from the environment (source ~/.hermes/.env first). ---
MODELS = {
    "model_a": {
        "url": "https://api.example.com/v1/chat/completions",
        "key_env": "MODEL_A_KEY",          # env var name, NOT the key value
        "model_id": "vendor/model-a",
    },
    "model_b": {
        "url": "https://openrouter.ai/api/v1/chat/completions",
        "key_env": "OPENROUTER_API_KEY",
        "model_id": "vendor/model-b",
    },
}
MAX_TOKENS = 4096  # reasoning models: this cap covers thinking + answer

with open(os.path.join(BASE, "questions.json")) as f:
    DATA = json.load(f)
SYSTEM, QUESTIONS = DATA["system_prompt"], DATA["questions"]


def call(model_name, question, retries=1):
    m = MODELS[model_name]
    body = {
        "model": m["model_id"],
        "messages": [
            {"role": "system", "content": SYSTEM},
            {"role": "user", "content": question["question"]},
        ],
        "temperature": 0,
        "max_tokens": MAX_TOKENS,
        "stream": False,
    }
    req = urllib.request.Request(
        m["url"], data=json.dumps(body).encode(),
        headers={"Authorization": f"Bearer {os.environ[m['key_env']]}",
                 "Content-Type": "application/json"},
        method="POST",
    )
    for attempt in range(retries + 1):
        try:
            with urllib.request.urlopen(req, timeout=600) as resp:
                return json.loads(resp.read().decode()), None
        except urllib.error.HTTPError as e:
            if attempt < retries:
                print(f"  [{model_name}] q{question['id']} HTTP {e.code} -- retrying", flush=True)
                time.sleep(5)
                continue
            return None, f"HTTP {e.code}: {e.read().decode()[:500]}"
        except Exception as e:
            if attempt < retries:
                print(f"  [{model_name}] q{question['id']} {e} -- retrying", flush=True)
                time.sleep(5)
                continue
            return None, str(e)
    return None, "unknown"


def main():
    only = sys.argv[1] if len(sys.argv) > 1 else None
    for model_name in MODELS:
        if only and model_name != only:
            continue
        print(f"=== {model_name} ({MODELS[model_name]['model_id']}) ===", flush=True)
        for q in QUESTIONS:
            fn = os.path.join(RAW, f"{model_name}_q{q['id']}.json")
            if os.path.exists(fn):
                print(f"  q{q['id']}: cached, skipping", flush=True)
                continue
            t0 = time.time()
            resp, err = call(model_name, q)
            dt = time.time() - t0
            with open(fn, "w") as f:
                json.dump(resp if not err else {"error": err, "question": q}, f, indent=2)
            if err:
                print(f"  q{q['id']}: FAILED ({dt:.0f}s): {err[:150]}", flush=True)
                continue
            u = resp.get("usage", {})
            fin = resp.get("choices", [{}])[0].get("finish_reason")
            print(f"  q{q['id']}: OK ({dt:.0f}s) prompt={u.get('prompt_tokens')} completion={u.get('completion_tokens')} finish={fin}", flush=True)
            time.sleep(1)  # politeness gap


if __name__ == "__main__":
    main()
