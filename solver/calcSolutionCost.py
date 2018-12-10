from createPath import create_path


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

    c = 0

    for s in path:
        c += cd[s]

    return c


def main():
    from SolutionExplorer import load_solution
    from UnitCost import default_unit_cost
    import sys

    if len(sys.argv) < 2:
        print("no solution file argument given")
        return
    _, solution = load_solution(sys.argv[1])
    print(calc_solution_cost(solution, default_unit_cost))


if __name__ == '__main__':
    main()
