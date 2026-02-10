import os, json, time

def export_run_artifacts(run_dir: str, entries: list):
    os.makedirs(run_dir, exist_ok=True)

    # Build stability series from entries (best-effort)
    series = []
    for e in entries:
        shared = e.get("shared", {}) or {}
        gate = shared.get("_gate", {}) or {}
        spawn = shared.get("_spawn", {}) or {}

        series.append({
            "ts": e.get("ts"),
            "step": e.get("step"),
            "alpha": gate.get("alpha"),
            "alpha_eff": gate.get("alpha_eff"),
            "gate_status": gate.get("status"),
            "spawned": (spawn.get("agents") if isinstance(spawn, dict) else None),
        })

    with open(os.path.join(run_dir, "stability_series.json"), "w", encoding="utf-8") as f:
        json.dump(series, f, indent=2)

    # Topology snapshot (who is active, what spawned, last gate state)
    topo = {
        "generated_at": time.time(),
        "last_step": (series[-1]["step"] if series else None),
        "agents_seen": sorted(list({a for s in series for a in (s.get("spawned") or [])})),
        "last_gate": (series[-1] if series else None)
    }

    with open(os.path.join(run_dir, "topology.json"), "w", encoding="utf-8") as f:
        json.dump(topo, f, indent=2)

    # Human summary
    contracting = [s for s in series if s.get("gate_status") == "CONTRACTING"]
    with open(os.path.join(run_dir, "summary.txt"), "w", encoding="utf-8") as f:
        f.write(f"entries={len(series)}\n")
        f.write(f"contracting_steps={len(contracting)}\n")
        if series:
            f.write(f"last_step={series[-1]['step']}\n")
            f.write(f"last_alpha_eff={series[-1].get('alpha_eff')}\n")
            f.write(f"last_gate_status={series[-1].get('gate_status')}\n")
