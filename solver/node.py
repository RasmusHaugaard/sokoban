import numpy as np
import collections

class Node:
    def __init__(self, map, r_pos_x, r_pos_y):
        self.map = map.copy()
        self.r_pos_x = r_pos_x
        self.r_pos_y = r_pos_y
        self.depth = 0
        self.parent = -1
        self.action = "no action"
        self.nodeID = 0
        self.manhatten = self.setManhatten()
        #self.manhatten = 0

    def up(self):

        if ((self.map[self.r_pos_y-1,self.r_pos_x]==b'X') or (((self.map[self.r_pos_y-1,self.r_pos_x]==b'J') or (self.map[self.r_pos_y-1,self.r_pos_x]==b'#')) and (self.map[self.r_pos_y-2,self.r_pos_x]==b'X' or self.map[self.r_pos_y-2,self.r_pos_x]==b'J' or self.map[self.r_pos_y-2,self.r_pos_x]==b'#'))):   # Path blocked
            #print("Path blocked")
            return 1                          
        else:                                                                                                           # Path not blocked
            if (self.map[self.r_pos_y-1,self.r_pos_x] == b'J' or self.map[self.r_pos_y-1,self.r_pos_x] == b'#'):        # Diamond
                if (self.map[self.r_pos_y-2,self.r_pos_x] == b'G'):                                                     # Push on goal                   
                    self.map[self.r_pos_y-2,self.r_pos_x] = b'#'          
                else :                                                                                                  # Push                        
                    self.map[self.r_pos_y-2,self.r_pos_x] = b'J'
                #print("Pushing diamond up")
            #else :                                                                                                      # Move up
                #print("Up")
        
            if (self.map[self.r_pos_y-1,self.r_pos_x] == b'#' or self.map[self.r_pos_y-1,self.r_pos_x] == b'G'):        # Move on goal
                self.map[self.r_pos_y-1,self.r_pos_x] = b'W'
            else :
                self.map[self.r_pos_y-1,self.r_pos_x] = b'M'

            if (self.map[self.r_pos_y,self.r_pos_x] == b'W'):                                                           # Standing on goal
                self.map[self.r_pos_y,self.r_pos_x] = b'G'
            else :   
                self.map[self.r_pos_y,self.r_pos_x] = b'.'
        
            self.r_pos_y = self.r_pos_y-1
            self.depth += 1
            self.action = "up"
            return 0

    def down(self):

        if ((self.map[self.r_pos_y+1,self.r_pos_x]==b'X') or (((self.map[self.r_pos_y+1,self.r_pos_x]==b'J') or (self.map[self.r_pos_y+1,self.r_pos_x]==b'#')) and (self.map[self.r_pos_y+2,self.r_pos_x]==b'X' or self.map[self.r_pos_y+2,self.r_pos_x]==b'J' or self.map[self.r_pos_y+2,self.r_pos_x]==b'#'))):   # Path blocked
            #print("Path blocked")
            return 1                          
        else:                                                                                                           # Path not blocked
            if (self.map[self.r_pos_y+1,self.r_pos_x] == b'J' or self.map[self.r_pos_y+1,self.r_pos_x] == b'#'):        # Diamond
                if (self.map[self.r_pos_y+2,self.r_pos_x] == b'G'):                                                     # Push on goal                   
                    self.map[self.r_pos_y+2,self.r_pos_x] = b'#'          
                else :                                                                                                  # Push                        
                    self.map[self.r_pos_y+2,self.r_pos_x] = b'J'
                #print("Pushing diamond down")
            #else :                                                                                                      # Move down
                #print("Down")
        
            if (self.map[self.r_pos_y+1,self.r_pos_x] == b'#' or self.map[self.r_pos_y+1,self.r_pos_x] == b'G'):        # Move on goal
                self.map[self.r_pos_y+1,self.r_pos_x] = b'W'
            else :
                self.map[self.r_pos_y+1,self.r_pos_x] = b'M'

            if (self.map[self.r_pos_y,self.r_pos_x] == b'W'):                                                           # Standing on goal
                self.map[self.r_pos_y,self.r_pos_x] = b'G'
            else :   
                self.map[self.r_pos_y,self.r_pos_x] = b'.'
        
            self.r_pos_y = self.r_pos_y+1
            self.depth += 1
            self.action = "down"
            return 0

    def right(self):

        if ((self.map[self.r_pos_y,self.r_pos_x+1]==b'X') or (((self.map[self.r_pos_y,self.r_pos_x+1]==b'J') or (self.map[self.r_pos_y,self.r_pos_x+1]==b'#')) and (self.map[self.r_pos_y,self.r_pos_x+2]==b'X' or self.map[self.r_pos_y,self.r_pos_x+2]==b'J' or self.map[self.r_pos_y,self.r_pos_x+2]==b'#'))):   # Path blocked
            #print("Path blocked")
            return 1                          
        else:                                                                                                           # Path not blocked
            if (self.map[self.r_pos_y,self.r_pos_x+1] == b'J' or self.map[self.r_pos_y,self.r_pos_x+1] == b'#'):        # Diamond
                if (self.map[self.r_pos_y,self.r_pos_x+2] == b'G'):                                                     # Push on goal                   
                    self.map[self.r_pos_y,self.r_pos_x+2] = b'#'          
                else :                                                                                                  # Push                        
                    self.map[self.r_pos_y,self.r_pos_x+2] = b'J'
                #print("Pushing diamond right")
            #else :                                                                                                      # Move right
                #print("Right")
        
            if (self.map[self.r_pos_y,self.r_pos_x+1] == b'#' or self.map[self.r_pos_y,self.r_pos_x+1] == b'G'):        # Move on goal
                self.map[self.r_pos_y,self.r_pos_x+1] = b'W'
            else :
                self.map[self.r_pos_y,self.r_pos_x+1] = b'M'

            if (self.map[self.r_pos_y,self.r_pos_x] == b'W'):                                                           # Standing on goal
                self.map[self.r_pos_y,self.r_pos_x] = b'G'
            else :   
                self.map[self.r_pos_y,self.r_pos_x] = b'.'
        
            self.r_pos_x = self.r_pos_x+1
            self.depth += 1
            self.action = "right"
            return 0

    def left(self):

        if ((self.map[self.r_pos_y,self.r_pos_x-1]==b'X') or (((self.map[self.r_pos_y,self.r_pos_x-1]==b'J') or (self.map[self.r_pos_y,self.r_pos_x-1]==b'#')) and (self.map[self.r_pos_y,self.r_pos_x-2]==b'X' or self.map[self.r_pos_y,self.r_pos_x-2]==b'J' or self.map[self.r_pos_y,self.r_pos_x-2]==b'#'))):   # Path blocked
            #print("Path blocked")
            return 1                          
        else:                                                                                                           # Path not blocked
            if (self.map[self.r_pos_y,self.r_pos_x-1] == b'J' or self.map[self.r_pos_y,self.r_pos_x-1] == b'#'):        # Diamond
                if (self.map[self.r_pos_y,self.r_pos_x-2] == b'G'):                                                     # Push on goal                   
                    self.map[self.r_pos_y,self.r_pos_x-2] = b'#'          
                else :                                                                                                  # Push                        
                    self.map[self.r_pos_y,self.r_pos_x-2] = b'J'
                #print("Pushing diamond left")
            #else :                                                                                                      # Move left
                #print("Left")
        
            if (self.map[self.r_pos_y,self.r_pos_x-1] == b'#' or self.map[self.r_pos_y,self.r_pos_x-1] == b'G'):        # Move on goal
                self.map[self.r_pos_y,self.r_pos_x-1] = b'W'
            else :
                self.map[self.r_pos_y,self.r_pos_x-1] = b'M'

            if (self.map[self.r_pos_y,self.r_pos_x] == b'W'):                                                           # Standing on goal
                self.map[self.r_pos_y,self.r_pos_x] = b'G'
            else :   
                self.map[self.r_pos_y,self.r_pos_x] = b'.'
        
            self.r_pos_x = self.r_pos_x-1
            self.depth += 1
            self.action = "left"
            return 0


    def up_test(self):

        if ((self.map[self.r_pos_y-1,self.r_pos_x]==b'X') or (((self.map[self.r_pos_y-1,self.r_pos_x]==b'J') or (self.map[self.r_pos_y-1,self.r_pos_x]==b'#')) and (self.map[self.r_pos_y-2,self.r_pos_x]==b'X' or self.map[self.r_pos_y-2,self.r_pos_x]==b'J' or self.map[self.r_pos_y-2,self.r_pos_x]==b'#'))):   # Path blocked
            return 1                          
        else:
            return 0

    def down_test(self):

        if ((self.map[self.r_pos_y+1,self.r_pos_x]==b'X') or (((self.map[self.r_pos_y+1,self.r_pos_x]==b'J') or (self.map[self.r_pos_y+1,self.r_pos_x]==b'#')) and (self.map[self.r_pos_y+2,self.r_pos_x]==b'X' or self.map[self.r_pos_y+2,self.r_pos_x]==b'J' or self.map[self.r_pos_y+2,self.r_pos_x]==b'#'))):   # Path blocked
            return 1                          
        else:
            return 0

    def right_test(self):

        if ((self.map[self.r_pos_y,self.r_pos_x+1]==b'X') or (((self.map[self.r_pos_y,self.r_pos_x+1]==b'J') or (self.map[self.r_pos_y,self.r_pos_x+1]==b'#')) and (self.map[self.r_pos_y,self.r_pos_x+2]==b'X' or self.map[self.r_pos_y,self.r_pos_x+2]==b'J' or self.map[self.r_pos_y,self.r_pos_x+2]==b'#'))):   # Path blocked
            return 1                          
        else:
            return 0

    def left_test(self):

        if ((self.map[self.r_pos_y,self.r_pos_x-1]==b'X') or (((self.map[self.r_pos_y,self.r_pos_x-1]==b'J') or (self.map[self.r_pos_y,self.r_pos_x-1]==b'#')) and (self.map[self.r_pos_y,self.r_pos_x-2]==b'X' or self.map[self.r_pos_y,self.r_pos_x-2]==b'J' or self.map[self.r_pos_y,self.r_pos_x-2]==b'#'))):   # Path blocked
            return 1                          
        else: 
            return 0

    def goal(self, number_diamonds):

        self.diamonds = number_diamonds
        self.diamonds_on_goal = self.map.count(b'#').sum() # Count diamonds in goal positions

        #print(self.map.count(b'#'))
        #print(self.map.count(b'#').sum())   
        #print("Diamonds on goal:" , self.diamonds_on_goal)

        if (self.diamonds_on_goal == self.diamonds):
            #print("Goal condition met")
            return 0
        else :
            #print("Goal condition not met")
            return 1

    def setManhatten(self):
        self.manhatten = 0
        self.buffer = []

        self.diamond_mask = self.map.count(b'J')
        #self.diamond_mask += self.map.count(b'#')
        self.diamonds = np.transpose(np.nonzero(self.diamond_mask))


        self.goal_mask = self.map.count(b'G')
        self.goal_mask += self.map.count(b'W')
        #self.goal_mask += self.map.count(b'#')
        self.goals = np.transpose(np.nonzero(self.goal_mask))

        #print(self.diamonds)
        #print(self.goals)
        #print(self.map)

        #print(self.diamonds[0])

        if (np.size(self.diamonds) >= 4):         
            for i in range(np.shape(self.diamonds)[0]):
                for j in range(np.shape(self.diamonds)[1]):
                    self.buffer.append(abs(self.diamonds[i,0] - self.goals[j,0]) + abs(self.diamonds[i,1] - self.goals[j,1]))
            
                self.manhatten += min(self.buffer)
                del self.buffer[:]

        elif (np.size(self.diamonds) == 2):
            self.manhatten = abs(self.diamonds[0][0] - self.goals[0][0]) + abs(self.diamonds[0][1] - self.goals[0][1])
            
                #self.manhatten += min(self.buffer)
                #del self.buffer[:]



            
            #print(self.manhatten)

        #return 0
        
        
    def setNodeID(self, val):
        self.nodeID = val
        

    def setParent(self, parent):
        self.parent = parent
        
