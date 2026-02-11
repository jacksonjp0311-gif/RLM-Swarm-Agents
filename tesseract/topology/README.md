# MODULE: tesseract/topology

## Purpose
Stores structural relationships between agents, modules, and invariants.

## Mini Directory
- structure.json → module topology model
- agents.json → agent lineage
- graph.json → structural relationships

## Inputs
- Agent spawn events
- Partition plans
- Structural summaries

## Outputs
- Graph model of swarm
- Historical topology snapshots

## Interactions
- agents
- partition
- invariants

## Stability Notes
Topology evolves additively.
Structural baseline hashes preserved.
