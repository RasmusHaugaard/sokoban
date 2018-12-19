import heapq
import numpy as np

from .AgentStateNodeExpander import AgentStateNodeExpander


class DiamondStateNodeExpander:
    def __init__(self, _map, unit_cost):
        self.expand = AgentStateNodeExpander(_map, unit_cost).call_with_diamond_map
        self.diamond_map = np.empty(_map.shape, dtype=np.int)
        self.diamond_map.fill(-1)

    def __call__(self, start_node):
        start_node_children = []

        _start_tot_cost = start_node.total_cost
        start_node.total_cost = start_node.current_cost

        for i, d in enumerate(start_node.diamonds):
            self.diamond_map[d] = i

        open_list = [start_node]
        closed_set = set()

        while open_list:
            parent = heapq.heappop(open_list)
            if parent.agent in closed_set:
                continue
            closed_set.add(parent.agent)
            if parent.diamonds is not start_node.diamonds:
                parent.parent = start_node
                start_node_children.append(parent)
                continue
            for child in self.expand(parent, self.diamond_map):
                child.total_cost = child.current_cost
                heapq.heappush(open_list, child)

        for d in start_node.diamonds:
            self.diamond_map[d] = -1

        start_node.total_cost = _start_tot_cost
        return start_node_children
