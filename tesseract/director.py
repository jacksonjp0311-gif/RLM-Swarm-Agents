import os, json, hashlib, datetime
from memory import memory_engine
from invariants import invariant_engine
from ledger import tesseract_ledger
from synthesis import synthesis_engine

RSAST_LEDGER = os.path.join('ledger','ledger.jsonl')

def load_rsast_ledger():
    if not os.path.exists(RSAST_LEDGER):
        return []
    with open(RSAST_LEDGER) as f:
        return [json.loads(x) for x in f if x.strip()]

def run_tesseract():
    entries = load_rsast_ledger()

    drift = memory_engine.compute_drift(entries)
    fingerprint = invariant_engine.compute_fingerprint(entries)
    tesseract_ledger.append_entry(drift, fingerprint)

    synthesis_engine.update_synthesis(drift)

    print("✔ Tesseract Updated")
    print("  Drift:", drift[-1] if drift else 0)
    print("  Fingerprint:", fingerprint[:12])

if __name__ == "__main__":
    run_tesseract()
