# MODULE: tesseract/config

## Purpose
Defines thresholds, contraction policies, and drift limits.

## Mini Directory
- tesseract_config.json → global settings
- thresholds.json → drift/pressure limits
- memory_rules.json → memory retention policies

## Inputs
- Stability policies
- Manual tuning

## Outputs
- Gate tightening parameters
- Drift alert thresholds

## Interactions
- coordination/gate
- monitoring
- memory

## Stability Notes
Configuration versioned.
Policy changes logged in ledger.
