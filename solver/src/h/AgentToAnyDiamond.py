from . import CostCache
from ...util import util

inf = float('inf')
ANY = util.ANY


def agent_to_any_diamond(agent_move_cost_cache, goal_set, agent, diamonds):
    mi = inf
    for diamond in diamonds:
        if diamond in goal_set: continue
        move = agent + diamond + (ANY,)
        c = agent_move_cost_cache[move]
        if c < mi: mi = c
    if mi == inf: mi = 0
    return mi


class AgentToAnyDiamond:
    meta = ()

    def __init__(self, _map, unit_cost):
        self.goals_set = set(util.get_goals(_map))
        self.unit_cost = unit_cost
        self.agent_move_cost_cache = \
            CostCache.build_agent_move_cost_cache(_map, unit_cost)

    def __call__(self, state):
        h = agent_to_any_diamond(self.agent_move_cost_cache, self.goals_set, state.agent, state.diamonds)
        return h, ()


def main():
    from ..MapLoader import load_map
    from ..UnitCost import default_unit_cost

    for map_path in ['test-map1.txt', 'test-map2.txt', 'test-map3.txt', 'test-map4.txt', 'test-map5.txt']:
        _map, init_states = load_map('solver/maps/' + map_path)
        heuristic = AgentToAnyDiamond(_map, default_unit_cost)
        h, _ = heuristic(init_states[0])
        print(map_path, h)


if __name__ == '__main__':
    main()
