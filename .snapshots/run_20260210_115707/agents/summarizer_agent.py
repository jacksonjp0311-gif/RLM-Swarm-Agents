class SummarizerAgent:
    def act(self, state):
        keys = sorted(list(state.shared.keys()))
        state.shared["summary"] = f"keys={len(keys)}:{','.join(keys[:12])}"
        return state
