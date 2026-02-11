# MODULE: tesseract/ledger

## Purpose
Append-only hash-chained cross-run memory ledger.

## Mini Directory
- tesseract_ledger.py → append engine
- tesseract_ledger.jsonl → immutable memory chain

## Inputs
- Drift metrics
- Invariant fingerprints
- Run summaries

## Outputs
- Hash-chained ledger entries
- Replay continuity record

## Interactions
- memory
- invariants
- synthesis

## Stability Notes
Hash chain: h_k = H(h_(k-1) || entry_k)
Ledger corruption must fail replay.
Never rewrite historical lines.
