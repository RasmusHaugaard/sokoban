from .createPath import create_path


def calc_solution_cost(solution, unit_cost):
    path = create_path(solution)
    path = path.replace('ll', 'u').replace('rr', 'u')
    path = path.replace('r', 't').replace('l', 't')
    path = path.replace('P', '')

    cd = {
        'f': unit_cost.forward,
        't': unit_cost.turn,
        'u': unit_cost.u_turn,
        'F': unit_cost.forward_diamond,
        'p': unit_cost.push,
    }

    cur_c = 0
    node_path_costs = [cur_c]
    for s in path:
        cur_c += cd[s]
        if s == 'f' or s == 'F':
            node_path_costs.append(cur_c)

    return node_path_costs


def main():
    from .exploreSolution import load_solution
    from ..src.UnitCost import default_unit_cost
    import sys

    if len(sys.argv) < 2:
        print("no solution file argument given")
        return
    _, solution = load_solution(sys.argv[1])
    print(calc_solution_cost(solution, default_unit_cost)[-1])


if __name__ == '__main__':
    main()
