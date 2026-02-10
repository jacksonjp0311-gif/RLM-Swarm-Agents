import os, json, time

def write_entry(run_dir, step, shared):
    os.makedirs(run_dir, exist_ok=True)
    path = os.path.join(run_dir, "ledger.jsonl")
    entry = {"ts": time.time(), "step": step, "shared": shared}
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")
