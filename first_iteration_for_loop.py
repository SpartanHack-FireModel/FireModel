
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


burned = [BURNING, BURNT, SMOLDERING]


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
    current_status = GREEN
    transition = FALSE
    crowning = false
    conditions = none
    new_status = GREEN
    burn_count = 0


#burns happen uphill




#algorithm determines T and C



#surface burn -slow fire : 


def set_board(burnable):
    new_board = np.zeros_like(game_board)


    for x in range(game_board.shape[0]):
        for y in range(game_board.shape[1]):    
            game_board[x,y] = Frame()
            game_board[x,y].wind_direction = wind_direction
            game_board[x,y].humidity = humidity


    return game_board




def getBurn(greenpixel):
  # if greenpixel * random > 0
  if(random.randint(1,255) < greenpixel):
    return 1

  return 0

def canBurn(x_spot,y_spot):
    if (game_board[x_spot,y_spot].biome >=5):
        return 1
    return 0




def advance_board(game_board):
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
            if(game_board[x,y] > 0):
                new_green[x,y] = game_board[x,y]
            if(redlayer[x,y] > 0):
                new_green[x,y] = 0
                new_red[x,y] = int(random.random() < .9)
                if(current_status == (BURNING)):
                    burn_count += 1

                    if(wind_direction == N):
                        if(game_board[x,y].conditions in [high, medium, low]):
                            if(canBurn(x, y+1)):
                                if(game_board[x, y+1].current_status not in burned):
                                    game_board[x, y+1].new_status = BURNING
                        if(game_board[x,y].conditions in [high, medium]):
                            if(canBurn(x+1, y+1)):
                                if(game_board[x+1, y+1].current_status not in burned):
                                    game_board[x+1, y+1].new_status = BURNING
                            if(canBurn(x-1, y+1)):
                                if(game_board[x-1, y+1].current_status not in burned):
                                    game_board[x-1, y+1].new_status = BURNING
                        if(game_board[x,y].conditions is high):
                            if(canBurn(x, y+2)):
                                if(game_board[x, y+2].current_status not in burned):
                                    game_board[x, y+2].new_status = BURNING
                            if(canBurn(x-1, y+2)):
                                if(game_board[x-1, y+2].current_status not in burned):
                                    game_board[x-1, y+2].new_status = BURNING
                            if(canBurn(x+1, y+2)):
                                if(game_board[x+1, y+2].current_status not in burned):
                                    game_board[x+1, y+2].new_status = BURNING

                    if(wind_direction == NE):
                        if(game_board[x,y].conditions in [high, medium, low]):
                            if(canBurn(x+1, y+1)):
                                if(game_board[x+1, y+1].current_status not in burned):
                                    game_board[x+1, y+1].new_status = BURNING
                        if(game_board[x,y].conditions in [high, medium]):
                            if(canBurn(x, y+1)):
                                if(game_board[x, y+1].current_status not in burned):
                                    game_board[x, y+1].new_status = BURNING
                            if(canBurn(x+1, y)):
                                if(game_board[x+1, y].current_status not in burned):
                                    game_board[x+1, y].new_status = BURNING
                        if(game_board[x,y].conditions == high):
                            if(canBurn(x+2, y+2)):
                                if(game_board[x+2, y+2].current_status not in burned):
                                    game_board[x+2, y+2].new_status = BURNING
                            if(canBurn(x, y+2)):
                                if(game_board[x, y+2].current_status not in burned):
                                    game_board[x, y+2].new_status = BURNING
                            if(canBurn(x+2, y)):
                                if(game_board[x+2, y].current_status not in burned):
                                    game_board[x+2, y].new_status = BURNING

                    if(wind_direction == E):
                        if(game_board[x,y].conditions in [high, medium, low]):
                            if(canBurn(x+1, y)):
                                if(game_board[x+1, y].current_status not in burned):
                                    game_board[x+1, y].new_status = BURNING
                        if(game_board[x,y].conditions in [high, medium]):
                            if(canBurn(x+1, y+1)):
                                if(game_board[x+1, y+1].current_status not in burned):
                                    game_board[x+1, y+1].new_status = BURNING
                            if(canBurn(x+1, y)):
                                if(game_board[x+1, y-1].current_status not in burned):
                                    game_board[x+1, y-1].new_status = BURNING
                        if(game_board[x,y].conditions == high):
                            if(canBurn(x+2, y+2)):
                                if(game_board[x+2, y+1].current_status not in burned):
                                    game_board[x+2, y+1].new_status = BURNING
                            if(canBurn(x, y+2)):
                                if(game_board[x+2, y-1].current_status not in burned):
                                    game_board[x+2, y-1].new_status = BURNING
                            if(canBurn(x+2, y)):
                                if(game_board[x+2, y].current_status not in burned):
                                    game_board[x+2, y].new_status = BURNING

                    if(wind_direction == SE):
                        if(game_board[x,y].conditions in [high, medium, low]):
                            if(canBurn(x+1, y-1)):
                                if(game_board[x+1, y-1].current_status not in burned):
                                    game_board[x+1, y-1].new_status = BURNING
                        if(game_board[x,y].conditions in [high, medium]):
                            if(canBurn(x, y-1)):
                                if(game_board[x, y-1].current_status not in burned):
                                    game_board[x, y-1].new_status = BURNING
                            if(canBurn(x+1, y)):
                                if(game_board[x+1, y-1].current_status not in burned):
                                    game_board[x+1, y-1].new_status = BURNING
                        if(game_board[x,y].conditions == high):
                            if(canBurn(x+2, y-2)):
                                if(game_board[x+2, y-2].current_status not in burned):
                                    game_board[x+2, y-2].new_status = BURNING
                            if(canBurn(x, y-2)):
                                if(game_board[x, y-2].current_status not in burned):
                                    game_board[x, y-2].new_status = BURNING
                            if(canBurn(x+2, y)):
                                if(game_board[x+2, y].current_status not in burned):
                                    game_board[x+2, y].new_status = BURNING                            


                    if(wind_direction == S):
                        if(game_board[x,y].conditions in [high, medium, low]):
                            if(canBurn(x, y-1)):
                                if(game_board[x, y-1].current_status not in burned):
                                    game_board[x, y-1].new_status = BURNING
                        if(game_board[x,y].conditions in [high, medium]):
                            if(canBurn(x-1, y-1)):
                                if(game_board[x-1, y-1].current_status not in burned):
                                    game_board[x-1, y-1].new_status = BURNING
                            if(canBurn(x+1, y-1)):
                                if(game_board[x+1, y-1].current_status not in burned):
                                    game_board[x+1, y-1].new_status = BURNING
                        if(game_board[x,y].conditions == high):
                            if(canBurn(x+1, y-2)):
                                if(game_board[x+1, y-2].current_status not in burned):
                                    game_board[x+1, y-2].new_status = BURNING
                            if(canBurn(x, y-2)):
                                if(game_board[x, y-2].current_status not in burned):
                                    game_board[x, y-2].new_status = BURNING
                            if(canBurn(x-1, y-2)):
                                if(game_board[x-1, y-2].current_status not in burned):
                                    game_board[x-1, y-2].new_status = BURNING 

                    if(wind_direction == SW):
                        if(game_board[x,y].conditions in [high, medium, low]):
                            if(canBurn(x-1, y-1)):
                                if(game_board[x-1, y-1].current_status not in burned):
                                    game_board[x-1, y-1].new_status = BURNING
                        if(game_board[x,y].conditions in [high, medium]):
                            if(canBurn(x, y-1)):
                                if(game_board[x, y-1].current_status not in burned):
                                    game_board[x, y-1].new_status = BURNING
                            if(canBurn(x-1, y)):
                                if(game_board[x-1, y].current_status not in burned):
                                    game_board[x-1, y].new_status = BURNING
                        if(game_board[x,y].conditions == high):
                            if(canBurn(x-2, y-2)):
                                if(game_board[x-2, y-2].current_status not in burned):
                                    game_board[x-2, y-2].new_status = BURNING
                            if(canBurn(x, y-2)):
                                if(game_board[x, y-2].current_status not in burned):
                                    game_board[x, y-2].new_status = BURNING
                            if(canBurn(x-2, y)):
                                if(game_board[x-2, y].current_status not in burned):
                                    game_board[x-2, y].new_status = BURNING 

                    if(wind_direction == W):
                        if(game_board[x,y].conditions in [high, medium, low]):
                            if(canBurn(x-1, y)):
                                if(game_board[x-1, y].current_status not in burned):
                                    game_board[x-1, y].new_status = BURNING
                        if(game_board[x,y].conditions in [high, medium]):
                            if(canBurn(x-1, y-1)):
                                if(game_board[x-1, y-1].current_status not in burned):
                                    game_board[x-1, y-1].new_status = BURNING
                            if(canBurn(x-1, y+1)):
                                if(game_board[x-1, y+1].current_status not in burned):
                                    game_board[x-1, y+1].new_status = BURNING
                        if(game_board[x,y].conditions == high):
                            if(canBurn(x-2, y-1)):
                                if(game_board[x-2, y-1].current_status not in burned):
                                    game_board[x-2, y-1].new_status = BURNING
                            if(canBurn(x-2, y-2)):
                                if(game_board[x-2, y+1].current_status not in burned):
                                    game_board[x-2, y+1].new_status = BURNING
                            if(canBurn(x-2, y)):
                                if(game_board[x-2, y].current_status not in burned):
                                    game_board[x-2, y].new_status = BURNING 

                    else: #NW
                        if(game_board[x,y].conditions in [high, medium, low]):
                            if(canBurn(x-1, y+1)):
                                if(game_board[x-1, y+1].current_status not in burned):
                                    game_board[x-1, y+1].new_status = BURNING
                        if(game_board[x,y].conditions in [high, medium]):
                            if(canBurn(x-1, y)):
                                if(game_board[x-1, y].current_status not in burned):
                                    game_board[x-1, y].new_status = BURNING
                            if(canBurn(x, y+1)):
                                if(game_board[x, y+1].current_status not in burned):
                                    game_board[x, y+1].new_status = BURNING
                        if(game_board[x,y].conditions == high):
                            if(canBurn(x-2, y+2)):
                                if(game_board[x-2, y+2].current_status not in burned):
                                    game_board[x-2, y+2].new_status = BURNING
                            if(canBurn(x-2, y)):
                                if(game_board[x-2, y].current_status not in burned):
                                    game_board[x-2, y].new_status = BURNING
                            if(canBurn(x, y+2)):
                                if(game_board[x, y+2].current_status not in burned):
                                    game_board[x, y+2].new_status = BURNING 


                if(current_status == SMOLDERING):
                    burn_count +=1    
                if(burn_count == 5):
                    new_status = SMOLDERING

                if(burn_count == 8):
                    new_status = BURNT
            
    
            # Now that we're inside the loops we need to apply our rules
        
            # if the cell was empty last turn, it's still empty.
            # if it was on fire last turn, it's now empty.
            
    
            # now, if there is a tree in the cell, we have to decide what to do
            
                
                # initially make the cell a tree in the new board
                

                # If one of the neighboring cells was on fire last turn, 
                # this cell is now on fire!
                # (make sure you account for whether or not you're on the edge!)
                
    for x in range(game_board.shape[0]):
        for y in range(game_board.shape[1]):
            game_board[x,y].current_status = new_status
            game_board[x,y].new_status = ""
    # return the new board
    return game_board




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

windspeed = 5
wind_direction = NE;
humidity = 0;

# 
on_fire = True

# Use a lovely for loop instead of a while loop
for i in range(100):

    # 
    board_size = 50
    game_board = set_fire(game_board)
    


    set_board(game_board)
    advance_board(game_board)


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









