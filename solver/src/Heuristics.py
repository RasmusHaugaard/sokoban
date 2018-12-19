from .h.DiamondClosest import DiamondClosest
from .h.AgentClosest import AgentClosest
from .h.Closest import Closest

from .h.MinMatchingDiamondToGoal import MinMatchingDiamondToGoal
from .h.MinMatchingAgentToDiamond import MinMatchingAgentToDiamond
from .h.MinMatching import MinMatching

from .h.AgentToAnyDiamond import AgentToAnyDiamond
from .h.MinMatchingPlus import MinMatchingPlus

from .h.BFS import BFS


_heuristics = {
    'd_closest': DiamondClosest,
    'a_closest': AgentClosest,
    'closest': Closest,

    'min_match_d2g': MinMatchingDiamondToGoal,
    'min_match_a2d': MinMatchingAgentToDiamond,
    'min_match': MinMatching,

    'a2any_d': AgentToAnyDiamond,
    'min_match+': MinMatchingPlus,

    'bfs': BFS
}

heuristic_keys = ['d_closest', 'closest', 'min_match_d2g', 'min_match', 'min_match+']


def get_heuristic(key):
    return _heuristics[key]
