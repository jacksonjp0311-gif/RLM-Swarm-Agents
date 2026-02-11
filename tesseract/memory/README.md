# MODULE: tesseract/memory

## Purpose
Tracks rolling drift history and persistent state vectors across runs.

## Mini Directory
- memory_engine.py → drift computation
- memory.json → long-term state vector
- drift_history.json → cross-run drift log

## Inputs
- RSAST ledger entries
- State transitions

## Outputs
- Drift history (Δ state)
- Persistent memory state

## Interactions
- invariants
- ledger
- synthesis

## Stability Notes
Drift accumulation is append-only.
Historical drift values are never altered.
