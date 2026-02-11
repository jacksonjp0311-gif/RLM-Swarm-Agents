# MODULE: tesseract/invariants

## Purpose
Maintains canonical invariant fingerprints across runs.

## Mini Directory
- invariant_engine.py → fingerprint computation
- checksums.json → baseline + delta hashes
- specs/ → canonical invariant documents

## Inputs
- RSAST state snapshots
- Schema contracts

## Outputs
- SHA256 invariant fingerprint
- Drift-by-hash metrics (D^(H))

## Interactions
- memory
- ledger
- monitoring

## Stability Notes
Invariant fingerprint must remain deterministic.
Hash deltas trigger drift alerts.
