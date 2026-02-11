# MODULE: tesseract/synthesis

## Purpose
Extracts learned patterns and stability heuristics from drift history.

## Mini Directory
- synthesis_engine.py → heuristic update logic
- heuristics.json → learned stability parameters
- optimizations.json → accumulated improvements

## Inputs
- Drift history
- Pressure metrics
- Stability scores

## Outputs
- Learned thresholds
- Stability trend metrics

## Interactions
- memory
- monitoring
- coordination/gate

## Stability Notes
Heuristics update additively.
No destructive overwrite of past runs.
