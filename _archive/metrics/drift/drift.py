def compute_drift(prev, curr):
    if not prev:
        return 0.0
    if prev == curr:
        return 0.0
    return 0.1
