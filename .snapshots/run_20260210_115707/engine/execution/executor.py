from agents.planner_agent import PlannerAgent
from agents.execution_agent import ExecutionAgent
from agents.invariant_agent import InvariantAgent
from agents.monitor_agent import MonitorAgent
from agents.stabilizer_agent import StabilizerAgent
from agents.summarizer_agent import SummarizerAgent

from metrics.pressure import compute_pressure
from metrics.drift import compute_drift
from coordination.gate.gate import apply_gate
from metrics.horizon import horizon

from tools.topology_memory import topo_event, memory_update

planner = PlannerAgent()
executor = ExecutionAgent()
inv = InvariantAgent()
mon = MonitorAgent()

stabilizer = StabilizerAgent()
summarizer = SummarizerAgent()

_prev_shared = {}

def step(state, mode="lab"):
    global _prev_shared

    state.step += 1

    planner.act(state)
    executor.act(state)
    inv.act(state)

    pressure = compute_pressure(state)
    drift = compute_drift(_prev_shared, state.shared)

    apply_gate(state, pressure, drift, alpha=0.85)
    h = horizon(0.85, pressure)

    spawned = []

    # Spawn policy
    if drift >= 0.1:
        stabilizer.act(state)
        spawned.append("StabilizerAgent")
    if pressure >= 0.85:
        summarizer.act(state)
        spawned.append("SummarizerAgent")

    if spawned:
        state.shared["_spawn"] = {"agents": spawned, "reason": {"drift": drift, "pressure": pressure}}

    gate_status = state.shared.get("_gate", {}).get("status", "OK")

    # record topology + memory every step (ACTIVE + LAB)
    topo_event(state.step, spawned, {"drift": drift, "pressure": pressure, "gate": gate_status})
    memory_update(gate_status, drift, pressure, spawned)

    # Print line (keep stable)
    print("ΔΦ:", drift, "Π:", round(pressure, 4), "H:", round(h, 2), "α_eff:", round(state.shared['_gate']['alpha_eff'], 4), gate_status)

    mon.act(state)

    _prev_shared = dict(state.shared)
    return state
