"""
The min-matching heuristic should calculate the actual
cost of test-map3 from the initial state.
"""

from MapLoader import load_map
from Solver import solve
from AgentStateNodeExpander import AgentStateNodeExpander as NodeExpander
from ClosestHeuristic import ClosestHeuristic as Heuristic
from UnitCost import default_unit_cost

_map, initial_states = load_map("test-map3.txt")

end_node = solve(_map, initial_states, NodeExpander, Heuristic, default_unit_cost)

heuristic = Heuristic(_map, default_unit_cost)

min_h = float('inf')
for node in initial_states:
    h = heuristic(node)
    if h < min_h: min_h = h

print('Init heuristic:', min_h)
print('Solution cost:', end_node.current_cost)
diff = min_h - end_node.current_cost
assert diff < 1e-10, 'test failed: {}'.format(diff)
print('test succeeded')
