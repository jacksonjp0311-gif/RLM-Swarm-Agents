class PlannerAgent:
    def act(self,state):
        state.shared["plan"]="active"
        return state
