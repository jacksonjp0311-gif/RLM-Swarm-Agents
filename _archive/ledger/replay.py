import json, os

LEDGER_PATH = os.path.join("ledger", "log.jsonl")

def iter_entries(path=LEDGER_PATH):
    if not os.path.exists(path):
        return
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                yield json.loads(line)
            except:
                continue

def replay_to_step(k: int, path=LEDGER_PATH):
    out = []
    for e in iter_entries(path):
        out.append(e)
        if int(e.get("step", -1)) >= k:
            break
    return out

def last_n(n: int, path=LEDGER_PATH):
    buf = []
    for e in iter_entries(path):
        buf.append(e)
    return buf[-n:]
