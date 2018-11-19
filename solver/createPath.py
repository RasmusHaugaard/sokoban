def createPath(solution):
    
    #print("Number of steps:", len(solution))
    
    #print("-----------------------------------------------")
    
    #if(solution[0].agent[2] == 0):
    #    init_direction = "up"
    #elif(solution[0].agent[2] == 1): 
    #    init_direction = "right"
    #elif(solution[0].agent[2] == 2):
    #    init_direction = "down"
    #elif(solution[0].agent[2] == 3):
    #    init_direction = "left"
        
    #print("Initial Agent orientation:", init_direction)
    
    path = ''
    
    for i in range(len(solution)-1):
        
        difference = solution[i].agent[2] - solution[i+1].agent[2]
        did_push = solution[i].diamonds != solution[i-1].diamonds
        
        if did_push and difference != 0:
            path += 'p'
            #print("push")
            
        if(difference == 1 or difference == -3):
            #print("left")
            path += 'l'
        elif(difference == -1 or difference == 3):
            #print("right")
            path += 'r'
        elif(difference == 2):
            #print("left")
            #print("left")
            path += 'll'
        elif(difference == -2):
            #print("right")
            #print("right")
            path += 'rr'
            
        #print("forward")
        path += 'f'
        
    path += 'p'
            
    #print(path)
    
    return path

def main():
    from SolutionExplorer import load_solution
    import sys
    
    if len(sys.argv) < 2:
        print("no solution file argument given")
        return
    _, solution = load_solution(sys.argv[1])
    print(createPath(solution))

if __name__ == '__main__':
    main()
