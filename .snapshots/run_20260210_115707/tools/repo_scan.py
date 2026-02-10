import os, hashlib, json

def scan_repo(path):
    digest = hashlib.sha256()

    file_count = 0
    total_size = 0

    for root, dirs, files in os.walk(path):
        for f in files:
            try:
                fp = os.path.join(root,f)
                data = open(fp,'rb').read()
                digest.update(data)
                file_count += 1
                total_size += len(data)
            except:
                pass

    return {
        "files": file_count,
        "size": total_size,
        "fingerprint": digest.hexdigest()
    }
