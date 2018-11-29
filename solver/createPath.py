def create_path(solution):
    path = ''

    for i in range(len(solution) - 1):

        difference = solution[i].agent[2] - solution[i + 1].agent[2]
        did_push = solution[i].diamonds != solution[i - 1].diamonds

        if did_push and difference != 0:
            path += 'p'

        if difference == 1 or difference == -3:
            path += 'l'
        elif difference == -1 or difference == 3:
            path += 'r'
        elif abs(difference) == 2:
            path += 'll'

        path += 'f'

    return path + 'P'


def main():
    from SolutionExplorer import load_solution
    import sys

    if len(sys.argv) < 2:
        print("no solution file argument given")
        return
    _, solution = load_solution(sys.argv[1])
    print(create_path(solution))


if __name__ == '__main__':
    main()
