import json, hashlib, os

def compute_fingerprint(entries):
    raw = json.dumps(entries, sort_keys=True).encode()
    fingerprint = hashlib.sha256(raw).hexdigest()

    os.makedirs('tesseract/invariants', exist_ok=True)
    with open('tesseract/invariants/checksums.json','w') as f:
        json.dump({'fingerprint':fingerprint},f,indent=2)

    return fingerprint
