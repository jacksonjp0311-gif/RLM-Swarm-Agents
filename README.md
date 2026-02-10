# RLM-Swarm-Agents

**Adaptive multi-agent execution system for repo analysis, restructuring, and stability monitoring**

---

## Overview

RLM-Swarm-Agents is a local-first multi-agent execution framework designed to:

* analyze repositories
* monitor structural drift and pressure
* propose safe patches
* generate restructure plans
* optionally apply changes with rollback support
* maintain a full execution ledger

The system operates in controlled phases and is built to remain:

* deterministic
* inspectable
* reversible
* safe-by-default

It is intended for advanced local development environments where automated code analysis and restructuring must occur without losing traceability.

---

## Core Capabilities

### 1. Active Mode

Analyzes a repository and produces:

* execution summaries
* patch proposals
* restructure plans
* topology + memory tracking

No changes are applied unless explicitly enabled.

---

### 2. Auto Mode

Extends Active Mode with:

* safe patch application
* snapshot creation before changes
* rollback capability
* apply logs

All modifications are reversible.

---

### 3. Watch Mode

Monitors a directory of repositories and:

* fingerprints repos
* detects drift
* generates reports
* optionally prepares restructuring

Useful for multi-repo environments.

---

## System Architecture

```
RLM_Swarm_Agents/
│
├─ agents/                 Core agent behaviors
├─ engine/                 Execution loop
├─ metrics/                Drift / pressure / horizon metrics
├─ coordination/           Gate + topology regulation
├─ tools/                  Patch + snapshot + scan utilities
├─ ledger/                 Execution logging
├─ runs/                   Per-run artifacts
├─ memory/                 Persistent system memory
├─ patches/                Proposed & applied patches
├─ topology/               Spawn + coordination history
├─ .snapshots/             Rollback snapshots
└─ run_swarm.py            Main entrypoint
```

---

## Execution Modes

### Active Mode

```
python run_swarm.py --mode active --steps 10
```

Produces:

* summary.md
* patch_proposals.diff
* restructure_plan.json
* monitor.json
* ledger.jsonl

No file modifications occur.

---

### Auto Mode

```
python run_swarm.py --mode auto --steps 10 --apply
```

Adds:

* snapshot creation
* safe patch application
* rollback capability

Snapshots stored in:

```
.snapshots/run_YYYYMMDD_HHMMSS/
```

Rollback:

```
python tools/rollback.py --snapshot ".snapshots/run_xxx"
```

---

### Watch Mode

Scan desktop or repo root:

```
python run_swarm.py --mode active --watch "C:\Users\...\Desktop"
```

Auto-apply safe scaffolding:

```
python run_swarm.py --mode auto --watch "C:\Users\...\Desktop" --apply
```

---

## Metrics

The system continuously evaluates:

| Metric       | Meaning                         |
| ------------ | ------------------------------- |
| ΔΦ (drift)   | Structural change between steps |
| Π (pressure) | Repo state complexity           |
| H (horizon)  | Stability horizon               |
| α_eff        | Adaptive coordination gate      |

These regulate agent spawning and restructuring behavior.

---

## Safety Model

Default behavior is **proposal-only**.

Changes occur only when:

```
--apply
```

Every apply run:

1. creates snapshot
2. logs applied patches
3. allows rollback

This ensures deterministic recoverability.

---

## Artifacts

Each run produces:

```
runs/run_YYYYMMDD_HHMMSS/
```

Containing:

* ledger.jsonl
* monitor.json
* summary.md
* patch_plan.json
* restructure_plan.json

Auto mode also creates:

```
.snapshots/run_xxx/
```

---

## Requirements

* Python 3.10+
* Git
* Local filesystem access

No external services required.

---

## Status

Current phase:
**Phase 8 — Active + Auto + Snapshot + Rollback**

System is stable for:

* local repo analysis
* restructuring proposals
* controlled auto-patching

---

## Philosophy

This framework is built around a simple rule:

> automation must remain reversible and inspectable

Every action must be logged.
Every change must be undoable.
Every proposal must be explicit.

---

## Author

James Paul Jackson
2026

---

## License

MIT (recommended) or project-specific.
