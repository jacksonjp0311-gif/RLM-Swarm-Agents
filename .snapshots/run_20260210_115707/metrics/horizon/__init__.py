def horizon(alpha, pressure):
    try:
        return 1.0 / ((1.0 - alpha) * (1.0 + pressure))
    except Exception:
        return 0.0
