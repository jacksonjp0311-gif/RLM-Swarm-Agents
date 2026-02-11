# MODULE: tesseract/snapshots

## Purpose
Deep checkpoint storage for rollback or branch exploration.

## Mini Directory
- checkpoint_###/ → archived state bundles
- latest.link → pointer to active snapshot

## Inputs
- Manual or automated checkpoint trigger

## Outputs
- Recoverable state images

## Interactions
- projections
- ledger

## Stability Notes
Snapshots immutable.
Used for controlled rollback only.
