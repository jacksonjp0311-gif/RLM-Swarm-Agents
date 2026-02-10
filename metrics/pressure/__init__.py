def compute_pressure(state):
    try:
        size = len(str(getattr(state, 'shared', {})))
    except Exception:
        size = 1
    return size / 1000.0
