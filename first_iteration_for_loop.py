
# coding: utf-8

# Board will be imported. Imagine a stack of 2D arrays, these will update with a for loop!
# 


import numpy as np
import numpy.random as rand
import matplotlib.pyplot as plt

# Next we are going to import some specific libraries we will use to get the animation to work cleanly
from IPython.display import display, clear_output
import time  

from PIL import Image








green = Image.open("server/pixel2.png")  #rename to image



threshold = 70  #Minimum green value for a space to be burnable

GREEN = (0,1,0)
RED = (1,0,0)
BLACK = (0,0,0)

colorvector = np.vectorize(lambda g: 0 if g < threshold else g)
greenlayer = np.array(green)[:,:,1]
burnable = colorvector(greenlayer)
print(burnable)

# gb = np.zeros((green.size[0], green.size[1],3))
# for x in range(green.size[0]):
#     for y in range(green.size[1]):
#         r, g, b = green.getpixel((x,y))
#         gb[x, y] = (0, int(g<threshold), 0)
        
# gb = np.rot90(gb)



# Function plotgrid() does what?? I believe it was to build an array the random number generators would populate

def plotgrid(myarray):
    
    plt.imshow(myarray)
    # 
    plt.ylim([0,myarray.shape[0]]) 
    plt.xlim([0,myarray.shape[1]])  #Defines the edges of our board

    # 
    plt.tick_params(axis='both', which='both',  #I believe this is stylistic editing
                    bottom='off', top='off', left='off', right='off',
                    labelbottom='off', labelleft='off')
    print(myarray)
    
plotgrid(greenlayer)
plt.show()
exit()

#status
BURNING = 1
SMOLDERING = 2
GREEN = 0
BURNT = 3
WATER = -1


#wind direction
N = 1
NE = 2
E = 3
SE = 4
S = 5
SW = 6
W = 7
NW = 8



#biomes
WATER = 0
URBAN = 1 #not flammable
ALPINE = 2 #not flammable
DESERT = 3 #not flammable
SHRUB = 4  #not flammable at all
MONTANE = 5 #2nd highest burn
CHAPARRAL = 6 #highest burn
CONIFEROUS = 7 #medium burn
SCRUB = 8 #low burn

#class for each frame of game board
#each frame should be one pixel of map
class Frame:
    windspeed = 0
    humidity = 0
    elevation = 0
    biome = 0
    wind_direction = NE
    status = GREEN
    transition = FALSE
    crowning = false
    conditions = none



#burns happen uphill




#algorithm determines T and C



#surface burn -slow fire : 


def set_board(burnable):
    windspeed = 5
    wind_direction = NE;
    humidity = 0;
    new_board = np.zeros_like(game_board)


    for x in range(game_board.shape[0]):
        for y in range(game_board.shape[1]):    
            game_board[x,y] = Frame()



    for x in range(game_board.shape[0]):
        for y in range(game_board.shape[1]):     

            if (x == 0 and y == 0):
                game_board[x,y].windspeed = 5
                game_board[x+1,y+1].windspeed = 5
                game_board[x+1,y].windspeed = 4
                game_board[x, y+1].windspeed = 4
                game_board[x, y].humidity = 1
            else:
                if(((x + xalt) < game_board.shape[0]) and 
                    (x+xalt) > 0 and
                    ((y + yalt) < game_board.shape[1]) and
                    (y + yalt > 0)):
                    if (game_board[x,y].windspeed != 0):
                        game_board[x+1,y+1].windspeed = game_board[x,y].windspeed
                        game_board[x+1,y].windspeed = game_board[x,y].windspeed - 1
                        game_board[x, y+1].windspeed = game_board[x,y].windspeed - 1
                        game_board[x, y].humidity = 1
                        if((windspeed - humidity - biome) >0):
                            crowning  = True
                        else:
                            crowning = False
                        if((windspeed + elevation - biome) > 0):
                            transition = True
                        else:
                            transition = False

                        #T and C determines Movement

                        #transition: fire moves up tree = more likely to move, medium/fast fire
                        #crowning : move across frames
                        #+T +C = moves super fast
                        #+T  -C = full stop, stays in place until burns out with no wind or wind moves it 
                        #-T -C =Surface Fire, very slow
                        #-T +C = Medium, Normal

                        if(transition and crowning):
                            game_board[x, y].conditions = high
                        elif(transition and not crowning):
                            game_board[x, y].conditions = stop
                        elif(not transition and crowning):
                            game_board[x, y].conditions = medium
                        elif(not transition and not crowning):
                            game_board[x, y].conditions = slow



def set_fire(game_board):
    '''
    Advances the game board using the given rules.
    Input: the initial game board.
    Output: the advanced game board
    '''
    
    # create a new array that's just like the original one, but initially set to all zeros (i.e., totally empty)
   
    
    # loop over each cell in the board and decide what to do.
    # You'll need two loops here, one nested inside the other.
    for x in range(game_board.shape[0]):
        for y in range(game_board.shape[1]):
            
            # Check for each pixel to equal to the pixel constants
            if(np.array_equal(game_board[x,y],BLACK)):
                new_board[x,y] == BLACK
                
            if(np.array_equal(game_board[x,y],RED)):
                new_board[x,y] == BLACK
                
            if(np.array_equal(game_board[x,y],GREEN)):
                new_board[x,y] = GREEN
                
                if x > 0:

                    if(np.array_equal(game_board[x-1,y] == RED)):

                        new_board[x,y] = RED
                        
                        

                if y > 0:

                    if(np.array_equal(game_board[x,y-1],RED)):

                        new_board[x,y] = RED

                if x < game_board.shape[0]-1:

                    if(np.array_equal(game_board[x+1,y],RED)):

                        new_board[x,y] = RED

                        

                if y < game_board.shape[1]-1:                    

                    if(np.array_equal(game_board[x,y+1],RED)):

                        new_board[x,y] = RED
                
            
    
            # Now that we're inside the loops we need to apply our rules
        
            # if the cell was empty last turn, it's still empty.
            # if it was on fire last turn, it's now empty.
            
    
            # now, if there is a tree in the cell, we have to decide what to do
            
                
                # initially make the cell a tree in the new board
                

                # If one of the neighboring cells was on fire last turn, 
                # this cell is now on fire!
                # (make sure you account for whether or not you're on the edge!)
                

    # return the new board
    return new_board



# In[41]:

# 
prob_tree=0.6
board_size = 50

#
fig = plt.figure(figsize=(10,10))

# 
game_board = gb
gb[0] = [RED]*(len(gb[1]))
# 
plotgrid(game_board)

# 
on_fire = True

# Use a lovely for loop instead of a while loop
for i in range(100):

    # 
    board_size = 50
    game_board = set_fire(game_board)
    
    # 
    plotgrid(game_board)
    time.sleep(0.05)  # 
    clear_output(wait=True)
    display(fig)
    fig.clear()

    # 


    # 


# 
plt.close()               









