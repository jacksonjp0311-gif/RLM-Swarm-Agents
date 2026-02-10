def alpha_eff(alpha, pressure, drift, frag=0.0):
    # α_eff = α (1 + Π) (1 + drift) (1 + frag)
    return alpha * (1.0 + pressure) * (1.0 + drift) * (1.0 + frag)

def apply_gate(state, pressure, drift, alpha=0.85):
    ae = alpha_eff(alpha, pressure, drift)
    gate = {"alpha": float(alpha), "alpha_eff": float(ae)}
    gate["status"] = "CONTRACTING" if ae >= 1.0 else "OK"
    state.shared["_gate"] = gate
    return state
