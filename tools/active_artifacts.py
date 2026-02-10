import os, json, hashlib

SKIP_DIRS = {'.git','__pycache__','.venv','node_modules','dist','build'}

def repo_tree(root, max_files=5000):
    root = os.path.abspath(root)
    items = []
    count = 0
    for r, dirs, files in os.walk(root):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for fn in files:
            fp = os.path.join(r, fn)
            rel = os.path.relpath(fp, root)
            try:
                size = os.path.getsize(fp)
            except Exception:
                size = -1
            items.append({"path": rel, "bytes": size})
            count += 1
            if count >= max_files:
                return items
    return items

def quick_hash(root, items):
    h = hashlib.sha256()
    for it in items:
        h.update(it["path"].encode("utf-8","ignore"))
        h.update(str(it["bytes"]).encode("utf-8"))
    return h.hexdigest()

def write_summary_md(out_path, root, items, fp_hash, mode, drift, pressure, gate_status, spawned):
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    items_sorted = sorted(items, key=lambda x: (x["bytes"] if x["bytes"] is not None else -1), reverse=True)
    top = items_sorted[:20]

    lines = []
    lines.append(f"# RLM Swarm Active Summary")
    lines.append("")
    lines.append(f"- Root: {root}")
    lines.append(f"- Mode: {mode}")
    lines.append(f"- Repo fingerprint: {fp_hash}")
    lines.append(f"- Drift ΔΦ: {drift}")
    lines.append(f"- Pressure Π: {pressure}")
    lines.append(f"- Gate: {gate_status}")
    lines.append(f"- Spawned: {', '.join(spawned) if spawned else 'none'}")
    lines.append("")
    lines.append("## Largest files (top 20)")
    for it in top:
        lines.append(f"- {it['path']} — {it['bytes']} bytes")
    lines.append("")

    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

def write_restructure_plan(out_json, root, items):
    # Safe-by-default: plan only. (No file moves unless --apply)
    # Heuristic: propose standard src/ layout if many top-level python files exist.
    os.makedirs(os.path.dirname(out_json), exist_ok=True)
    top_level_py = [it["path"] for it in items if (it["path"].count(os.sep) == 0 and it["path"].endswith(".py"))]
    plan = {
        "root": root,
        "recommendation": "none",
        "moves": [],
        "notes": []
    }
    if len(top_level_py) >= 5:
        plan["recommendation"] = "introduce_src_layout"
        for p in top_level_py:
            plan["moves"].append({"from": p, "to": os.path.join("src", p)})
        plan["notes"].append("Detected many top-level .py files; src/ layout improves packaging + imports.")
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(plan, f, indent=2)

def write_patch_proposals(out_diff, out_plan_json, root, items):
    # Safe patch proposals (unified diff) — focuses on packaging hygiene + encoding rules.
    os.makedirs(os.path.dirname(out_diff), exist_ok=True)

    proposals = []
    proposals.append({
        "id": "P001",
        "title": "Standardize UTF-8 encoding on writes",
        "rationale": "Avoid BOM/UTF16 artifacts causing UnicodeDecodeError during exports.",
        "patch": [
            "--- a/README.md",
            "+++ b/README.md",
            "@@",
            "+## Encoding",
            "+All generated artifacts are written as UTF-8 (no BOM) to avoid decode issues across Windows tooling."
        ]
    })

    proposals.append({
        "id": "P002",
        "title": "Add src/ layout (plan-only)",
        "rationale": "Improves import stability and makes packaging predictable.",
        "patch": [
            "--- a/README.md",
            "+++ b/README.md",
            "@@",
            "+## Suggested structure",
            "+Consider moving top-level python modules under src/ and using explicit packages."
        ]
    })

    # Write diff file (proposal-only)
    with open(out_diff, "w", encoding="utf-8") as f:
        for pr in proposals:
            f.write(f"# {pr['id']} — {pr['title']}\n")
            f.write(f"# Rationale: {pr['rationale']}\n")
            for line in pr["patch"]:
                f.write(line + "\n")
            f.write("\n")

    with open(out_plan_json, "w", encoding="utf-8") as f:
        json.dump({"root": root, "proposals": proposals}, f, indent=2)
