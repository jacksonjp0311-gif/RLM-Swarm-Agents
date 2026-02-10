import os, shutil, argparse

def restore_snapshot(snapshot_path, target="."):
    snapshot_path = os.path.abspath(snapshot_path)
    target = os.path.abspath(target)

    if not os.path.isdir(snapshot_path):
        raise SystemExit(f"Snapshot not found: {snapshot_path}")

    # wipe target except .git and .snapshots
    for name in os.listdir(target):
        if name in (".git", ".snapshots"):
            continue
        p = os.path.join(target, name)
        if os.path.isdir(p):
            shutil.rmtree(p, ignore_errors=True)
        else:
            try:
                os.remove(p)
            except Exception:
                pass

    # copy snapshot back
    for root, dirs, files in os.walk(snapshot_path):
        rel = os.path.relpath(root, snapshot_path)
        dst_dir = target if rel == "." else os.path.join(target, rel)
        os.makedirs(dst_dir, exist_ok=True)
        for fn in files:
            src = os.path.join(root, fn)
            dst = os.path.join(dst_dir, fn)
            shutil.copy2(src, dst)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--snapshot", required=True)
    ap.add_argument("--target", default=".")
    args = ap.parse_args()
    restore_snapshot(args.snapshot, args.target)
    print("✔ RESTORED SNAPSHOT:", args.snapshot)

if __name__ == "__main__":
    main()
