from ..src.MapLoader import WALL, AGENT, FLOOR, GOAL, DIAMOND, AGENT_ON_GOAL, DIAMOND_ON_GOAL

symbols = {
    WALL: '█',
    AGENT: 'M',
    AGENT_ON_GOAL: '@',
    FLOOR: ' ',
    GOAL: 'G',
    DIAMOND: 'J',
    DIAMOND_ON_GOAL: '#',
}


def draw_state(_map, state, width=2):
    _map = _map.copy()
    a = state.agent[:2]
    if _map[a] == GOAL:
        _map[a] = AGENT_ON_GOAL
    else:
        _map[a] = AGENT
    for diamond in state.diamonds:
        if _map[diamond] == GOAL:
            _map[diamond] = DIAMOND_ON_GOAL
        else:
            _map[diamond] = DIAMOND

    h, w = _map.shape
    for y in range(h):
        for x in range(w):
            if _map[y, x] == WALL:
                print(symbols[WALL] * width, end='')
            else:
                print(symbols[_map[y, x]], end='')
                print(' ' * (width - 1), end='')
        print('')


def main():
    from ..src.MapLoader import load_map
    from ..src.StateNode import StateNode
    _map, initial_states = load_map('solver/maps/2017-competition-map.txt')
    draw_state(_map, initial_states[0])
    state = StateNode(None, (1, 4, 0), ((3, 3), (3, 2)), 0)
    print('')
    draw_state(_map, state)


if __name__ == '__main__':
    main()
