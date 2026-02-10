class ExecutionAgent:
    def act(self,state):
        state.shared["exec"]="running"
        return state
