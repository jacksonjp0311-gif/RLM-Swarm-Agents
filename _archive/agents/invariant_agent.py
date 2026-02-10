import hashlib, json
class InvariantAgent:
    def act(self,state):
        h = hashlib.sha256(json.dumps(state.shared,sort_keys=True).encode()).hexdigest()
        state.shared["fingerprint"]=h
        return state
