class MonitorAgent:
    def act(self,state):
        print("MONITOR STEP", state.step)
        return state
