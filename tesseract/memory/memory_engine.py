import json, os

def compute_drift(entries):
    drift = []
    prev = None
    for e in entries:
        val = e.get('state',{}).get('value',0)
        if prev is None:
            drift.append(0)
        else:
            drift.append(abs(val-prev))
        prev = val

    os.makedirs('tesseract/memory', exist_ok=True)
    with open('tesseract/memory/drift_history.json','w') as f:
        json.dump(drift,f,indent=2)

    return drift
