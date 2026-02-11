# MODULE: tesseract/projections

## Purpose
Stores run-end projection bundles for deterministic replay + rollback.

## Mini Directory
- run_YYYY_MM_DD/ → per-run snapshot
- latest.json → pointer to most recent projection

## Inputs
- End-of-run state
- Summary artifacts
- Patch diffs

## Outputs
- Reconstructable run bundle
- Replay anchor

## Interactions
- ledger
- monitoring
- synthesis

## Stability Notes
Snapshots are immutable once written.
latest.json may update pointer only.
