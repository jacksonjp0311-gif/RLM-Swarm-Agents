import os, shutil, time, json, hashlib

SKIP_DIRS = {'.git','__pycache__','.venv','node_modules','dist','build','.snapshots'}

def _ts(prefix="run"):
    return f"{prefix}_{time.strftime('%Y%m%d_%H%M%S')}"

def snapshot_repo(root, out_dir=".snapshots", label=None):
    root = os.path.abspath(root)
    name = _ts("run") if not label else label
    snap = os.path.abspath(os.path.join(out_dir, name))
    os.makedirs(snap, exist_ok=True)

    for r, dirs, files in os.walk(root):
        rel = os.path.relpath(r, root)
        # skip snapshot directory itself + junk
        parts = set(rel.split(os.sep)) if rel != "." else set()
        if parts & SKIP_DIRS:
            dirs[:] = []
            continue

        # filter dirs in-place
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]

        dst_dir = os.path.join(snap, rel) if rel != "." else snap
        os.makedirs(dst_dir, exist_ok=True)

        for fn in files:
            if fn.endswith((".pyc",".pyo")):
                continue
            src = os.path.join(r, fn)
            dst = os.path.join(dst_dir, fn)
            try:
                shutil.copy2(src, dst)
            except Exception:
                # best-effort copy
                try:
                    shutil.copy(src, dst)
                except Exception:
                    pass

    return snap

def repo_fingerprint(root, max_files=20000):
    root = os.path.abspath(root)
    h = hashlib.sha256()
    n = 0
    for r, dirs, files in os.walk(root):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for fn in files:
            fp = os.path.join(r, fn)
            try:
                st = os.stat(fp)
            except Exception:
                continue
            rel = os.path.relpath(fp, root)
            h.update(rel.encode("utf-8","ignore"))
            h.update(str(st.st_size).encode("utf-8"))
            h.update(str(int(st.st_mtime)).encode("utf-8"))
            n += 1
            if n >= max_files:
                break
        if n >= max_files:
            break
    return h.hexdigest()

def append_apply_log(entry, path=os.path.join("patches","applied_log.jsonl")):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    entry = dict(entry)
    entry["ts"] = time.time()
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")

def ensure_utf8_no_bom(path, text):
    # Always write UTF-8 without BOM
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)

def safe_move(root, src_rel, dst_rel):
    root = os.path.abspath(root)
    src = os.path.join(root, src_rel)
    dst = os.path.join(root, dst_rel)
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    shutil.move(src, dst)

def apply_restructure_plan(plan_path, root=None):
    with open(plan_path, "r", encoding="utf-8") as f:
        plan = json.load(f)
    root = os.path.abspath(root or plan.get("root") or ".")
    moves = plan.get("moves", [])
    done = []
    for mv in moves:
        fr = mv.get("from")
        to = mv.get("to")
        if not fr or not to:
            continue
        src = os.path.join(root, fr)
        if not os.path.exists(src):
            continue
        safe_move(root, fr, to)
        done.append({"from": fr, "to": to})
    return {"root": root, "moved": done, "count": len(done)}

def apply_patch_plan(patch_plan_json, root=None):
    # Minimal safe patcher: apply only README.md insertions from our proposals.
    # (Extensible later)
    with open(patch_plan_json, "r", encoding="utf-8") as f:
        pp = json.load(f)
    root = os.path.abspath(root or pp.get("root") or ".")
    proposals = pp.get("proposals", [])
    applied = []
    for pr in proposals:
        if pr.get("id") == "P001":
            readme = os.path.join(root, "README.md")
            if not os.path.exists(readme):
                ensure_utf8_no_bom(readme, "# Repo\n\n")
            with open(readme, "r", encoding="utf-8", errors="ignore") as f:
                txt = f.read()
            if "## Encoding" not in txt:
                txt = txt.rstrip() + "\n\n## Encoding\nAll generated artifacts are written as UTF-8 (no BOM) to avoid decode issues across Windows tooling.\n"
                ensure_utf8_no_bom(readme, txt)
                applied.append(pr.get("id"))
        if pr.get("id") == "P002":
            # non-destructive note insertion
            readme = os.path.join(root, "README.md")
            if not os.path.exists(readme):
                ensure_utf8_no_bom(readme, "# Repo\n\n")
            with open(readme, "r", encoding="utf-8", errors="ignore") as f:
                txt = f.read()
            if "## Suggested structure" not in txt:
                txt = txt.rstrip() + "\n\n## Suggested structure\nConsider moving top-level python modules under src/ and using explicit packages.\n"
                ensure_utf8_no_bom(readme, txt)
                applied.append(pr.get("id"))
    return {"root": root, "applied": applied, "count": len(applied)}
