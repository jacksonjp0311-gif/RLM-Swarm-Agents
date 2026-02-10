import os, json, time

TOPO_PATH = os.path.join("topology", "topology.json")
MEM_PATH  = os.path.join("memory", "memory.json")

def _load_json(path, default):
    try:
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
    except Exception:
        pass
    return default

def _save_json(path, obj):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2)

def topo_event(step, spawned, reason):
    topo = _load_json(TOPO_PATH, {"events": []})
    topo["events"].append({
        "ts": time.time(),
        "step": step,
        "spawned": spawned,
        "reason": reason
    })
    _save_json(TOPO_PATH, topo)

def memory_update(gate_status, drift, pressure, spawned):
    mem = _load_json(MEM_PATH, {
        "runs": 0,
        "contracting_steps": 0,
        "ok_steps": 0,
        "spawn_counts": {},
        "last": {}
    })
    mem["runs"] = int(mem.get("runs", 0)) + 1
    if gate_status == "CONTRACTING":
        mem["contracting_steps"] = int(mem.get("contracting_steps", 0)) + 1
    else:
        mem["ok_steps"] = int(mem.get("ok_steps", 0)) + 1

    sc = mem.get("spawn_counts", {})
    for a in (spawned or []):
        sc[a] = int(sc.get(a, 0)) + 1
    mem["spawn_counts"] = sc

    mem["last"] = {
        "gate": gate_status,
        "drift": float(drift),
        "pressure": float(pressure),
        "spawned": list(spawned or [])
    }
    _save_json(MEM_PATH, mem)
