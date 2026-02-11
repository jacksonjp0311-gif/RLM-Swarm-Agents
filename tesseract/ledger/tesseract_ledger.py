import json, hashlib, os, datetime

LEDGER_FILE = 'tesseract/ledger/tesseract_ledger.jsonl'

def append_entry(drift, fingerprint):
    os.makedirs('tesseract/ledger', exist_ok=True)

    entry = {
        'timestamp': str(datetime.datetime.utcnow()),
        'last_drift': drift[-1] if drift else 0,
        'fingerprint': fingerprint
    }

    prev_hash = ''
    if os.path.exists(LEDGER_FILE):
        with open(LEDGER_FILE) as f:
            lines = f.readlines()
            if lines:
                prev_hash = json.loads(lines[-1])['hash']

    raw = json.dumps(entry, sort_keys=True).encode()
    h = hashlib.sha256(prev_hash.encode() + raw).hexdigest()

    entry['hash'] = h

    with open(LEDGER_FILE,'a') as f:
        f.write(json.dumps(entry)+'\n')
