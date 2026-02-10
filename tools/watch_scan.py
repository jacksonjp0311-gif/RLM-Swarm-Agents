import os, hashlib, json

SKIP_DIRS = {'.git','__pycache__','.venv','node_modules','dist','build'}

def _hash_file(fp, h):
    try:
        with open(fp,'rb') as f:
            while True:
                b = f.read(1024*1024)
                if not b: break
                h.update(b)
    except:
        return 0
    return 1

def fingerprint_repo(repo_path, max_files=20000):
    h = hashlib.sha256()
    files = 0
    bytes_total = 0

    for root, dirs, fs in os.walk(repo_path):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for name in fs:
            fp = os.path.join(root, name)
            try:
                size = os.path.getsize(fp)
            except:
                continue
            # fold path + size into fingerprint to capture structural change quickly
            h.update(os.path.relpath(fp, repo_path).encode('utf-8','ignore'))
            h.update(str(size).encode('utf-8'))
            ok = _hash_file(fp, h)
            if ok:
                files += 1
                bytes_total += size
            if files >= max_files:
                break
        if files >= max_files:
            break

    return {"files":files, "bytes":bytes_total, "fingerprint":h.hexdigest()}

def list_repos(root_dir):
    # repo = any directory containing .git OR pyproject/package signals
    repos = []
    for entry in os.listdir(root_dir):
        p = os.path.join(root_dir, entry)
        if not os.path.isdir(p): 
            continue
        if os.path.isdir(os.path.join(p, ".git")):
            repos.append(p)
            continue
        if os.path.exists(os.path.join(p, "pyproject.toml")) or os.path.exists(os.path.join(p, "package.json")):
            repos.append(p)
            continue
    return sorted(repos)

def watch_repos(root_dir):
    root_dir = os.path.abspath(root_dir)
    repos = list_repos(root_dir)
    out = {"root": root_dir, "repos": []}
    for rp in repos:
        fp = fingerprint_repo(rp)
        out["repos"].append({"name": os.path.basename(rp), "path": rp, **fp})
    return out
