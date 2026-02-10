class StabilizerAgent:
    def act(self, state):
        state.shared["stabilizer"] = {"status":"active","action":"tighten_gate_hint"}
        return state
