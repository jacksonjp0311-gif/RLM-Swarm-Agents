import sys, os, json, time
from runtime.swarm_state.swarm_state import SwarmState
from engine.execution.executor import step
from ledger.ledger import write_entry

def _run_dir():
    ts = time.strftime("run_%Y%m%d_%H%M%S")
    d = os.path.join("runs", ts)
    os.makedirs(d, exist_ok=True)
    return d

def _arg(name, default=None):
    if name in sys.argv:
        i = sys.argv.index(name)
        if i+1 < len(sys.argv):
            return sys.argv[i+1]
    return default

def _has(flag):
    return flag in sys.argv

def _mode():
    return _arg("--mode", "lab")

def _steps():
    s = _arg("--steps", None)
    return int(s) if s is not None else None

def main():
    mode = _mode()
    run_dir = _run_dir()
    apply = _has("--apply")

    # WATCH MODE: scan repos + write artifacts; AUTO can APPLY safe changes
    if "--watch" in sys.argv:
        root = _arg("--watch", None)
        if not root:
            print("ERROR: --watch requires a directory path")
            return

        from tools.watch_scan import watch_repos
        report = watch_repos(root)
        outp = os.path.join(run_dir, "watch_report.json")
        with open(outp, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2)

        print("WATCH ROOT:", report["root"])
        print("REPOS:", len(report["repos"]))

        # ACTIVE/AUTO artifacts for watched root
        if mode in ("active","auto"):
            from tools.active_artifacts import repo_tree, quick_hash, write_summary_md, write_patch_proposals, write_restructure_plan
            items = repo_tree(root)
            fp = quick_hash(root, items)
            write_summary_md(os.path.join(run_dir, "summary.md"), root, items, fp, mode, drift=0.0, pressure=0.0, gate_status="WATCH", spawned=[])
            write_patch_proposals(os.path.join(run_dir, "patch_proposals.diff"), os.path.join(run_dir, "patch_plan.json"), root, items)
            write_restructure_plan(os.path.join(run_dir, "restructure_plan.json"), root, items)

            # AUTO APPLY (safe) with FULL SNAPSHOT
            if mode == "auto" and apply:
                from tools.fs_apply import snapshot_repo, repo_fingerprint, apply_restructure_plan, apply_patch_plan, append_apply_log
                before_fp = repo_fingerprint(root)
                snap = snapshot_repo(root)
                # apply patches (README insertions) + restructure (file moves if plan suggests)
                pr = apply_patch_plan(os.path.join(run_dir,"patch_plan.json"), root=root)
                rs = apply_restructure_plan(os.path.join(run_dir,"restructure_plan.json"), root=root)
                after_fp = repo_fingerprint(root)
                append_apply_log({
                    "mode": "watch-auto",
                    "root": root,
                    "snapshot": snap,
                    "before_fp": before_fp,
                    "after_fp": after_fp,
                    "patch": pr,
                    "restructure": rs
                })

        print("✔ RUN COMPLETE:", run_dir)
        return

    # SWARM LOOP
    state = SwarmState()
    steps = _steps()
    if steps is None:
        steps = 10 if mode in ("lab","active") else 50

    for i in range(steps):
        state = step(state, mode=mode)
        write_entry(run_dir, state.step, state.shared)
        print("STEP", i)

    # ACTIVE/AUTO artifacts for this repo after run
    if mode in ("active","auto"):
        from tools.active_artifacts import repo_tree, quick_hash, write_summary_md, write_patch_proposals, write_restructure_plan
        root = os.path.abspath(".")
        items = repo_tree(root)
        fp = quick_hash(root, items)

        drift = float(state.shared.get("_spawn", {}).get("reason", {}).get("drift", 0.0)) if isinstance(state.shared.get("_spawn", {}), dict) else 0.0
        try:
            pressure = len(str(state.shared))/1000.0
        except Exception:
            pressure = 0.0

        gate_status = state.shared.get("_gate", {}).get("status", "OK")
        spawned = state.shared.get("_spawn", {}).get("agents", []) if isinstance(state.shared.get("_spawn", {}), dict) else []
        write_summary_md(os.path.join(run_dir, "summary.md"), root, items, fp, mode, drift, pressure, gate_status, spawned)
        write_patch_proposals(os.path.join(run_dir, "patch_proposals.diff"), os.path.join(run_dir, "patch_plan.json"), root, items)
        write_restructure_plan(os.path.join(run_dir, "restructure_plan.json"), root, items)

        # AUTO APPLY (safe) with FULL SNAPSHOT
        if mode == "auto" and apply:
            from tools.fs_apply import snapshot_repo, repo_fingerprint, apply_restructure_plan, apply_patch_plan, append_apply_log
            before_fp = repo_fingerprint(root)
            snap = snapshot_repo(root)
            pr = apply_patch_plan(os.path.join(run_dir,"patch_plan.json"), root=root)
            rs = apply_restructure_plan(os.path.join(run_dir,"restructure_plan.json"), root=root)
            after_fp = repo_fingerprint(root)
            append_apply_log({
                "mode": "repo-auto",
                "root": root,
                "snapshot": snap,
                "before_fp": before_fp,
                "after_fp": after_fp,
                "patch": pr,
                "restructure": rs
            })

    # Final monitor artifact
    outp = os.path.join(run_dir, "monitor.json")
    with open(outp, "w", encoding="utf-8") as f:
        json.dump({"step": state.step, "shared": state.shared}, f, indent=2)

    print("✔ RUN COMPLETE:", run_dir)

if __name__ == "__main__":
    main()
