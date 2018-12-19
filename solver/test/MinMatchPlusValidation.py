"""
The min-matching heuristic should calculate the actual
cost of test-map3(b) and test-map4 from the initial states.
"""

from ..src.MapLoader import load_map
from ..src.Solver import solve
from ..src.AgentStateNodeExpander import AgentStateNodeExpander as NodeExpander
from ..src.h.MinMatchingPlus import MinMatchingPlus as Heuristic
from ..src.UnitCost import default_unit_cost

c = {
    'f': default_unit_cost.forward,
    't': default_unit_cost.turn,
    'u': default_unit_cost.u_turn,
    'F': default_unit_cost.forward_diamond,
    'p': default_unit_cost.push
}

for map_path, opt_sol in (
        ('test-map3.txt', 'ffFFFFFprfFFprfFFFFFF'),
        ('test-map3b.txt', 'ffFFFFFprfFFFFprfffFFFF'),
        ('test-map3c.txt', 'ffFFFprfFprffFFF'),
        ('test-map4.txt', 'fFplfprfprf'),
):
    print('Map:', map_path)
    _map, initial_states = load_map('solver/maps/' + map_path)

    end_node = solve(_map, initial_states, NodeExpander, Heuristic, default_unit_cost)

    heuristic = Heuristic(_map, default_unit_cost)
    min_h = float('inf')
    for node in initial_states:
        h, _ = heuristic(node)
        if h < min_h: min_h = h

    exp_cost = 0
    opt_sol = opt_sol.replace('ll', 'u').replace('rr', 'u').replace('l', 't').replace('r', 't')
    for s in opt_sol:
        exp_cost += c[s]

    print('Expected cost:', exp_cost)
    print('Init heuristic:', min_h)
    print('Solution cost:', end_node.current_cost)
    h_diff = exp_cost - min_h
    s_diff = exp_cost - end_node.current_cost
    assert abs(h_diff) < 1e-10, 'heuristic test failed: {}'.format(h_diff)
    assert abs(s_diff) < 1e-10, 'solution test failed: {}'.format(s_diff)
    print('test succeeded\n')
