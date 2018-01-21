
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

import random
from multiprocessing import Process





mapImg = Image.open("../notebooks/map_crop.png")  #rename to image
biomeImg = Image.open("../notebooks/biome_crop.png") 
heightImg = Image.open("../notebooks/height_crop.png") 

biomeImg = np.array(biomeImg)
heightImg = np.array(heightImg)
threshold = 70  #Minimum green value for a space to be burnable

GREEN = (0,1,0)
RED = (1,0,0)
BLACK = (0,0,0)

colorvector = np.vectorize(lambda g: 0 if g < threshold else g)
mapVec = np.array(mapImg)
greenlayer = np.array(mapImg)[:,:,1]
burnable = colorvector(greenlayer)

# gb = np.zeros((green.size[0], green.size[1],3))
# for x in range(green.size[0]):
#     for y in range(green.size[1]):
#         r, g, b = green.getpixel((x,y))
#         gb[x, y] = (0, int(g<threshold), 0)
        
# gb = np.rot90(gb)



# Function plotgrid() does what?? I believe it was to build an array the random number generators would populate







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


#conditions
STOP = 0
LOW = 1
MEDIUM = 2
HIGH = 3


#biomes
WATER = 0
URBAN = 1 #not flammable
ALPINE = 2 #not flammable
DESERT = 3 #not flammable
SHRUB = 4  #not flammable at all
MONTANE = 5 #2nd HIGHest burn
CHAPARRAL = 6 #HIGHest burn
CONIFEROUS = 7 #medium burn
SCRUB = 8 #low burn

def plotgrid(myarray,frameNumber):
    
    imgData = np.zeros((myarray.shape[0],myarray.shape[1],3))
    for x in range(myarray.shape[0]):
        for y in range(myarray.shape[1]):
            if(myarray[x,y].current_status in burned):

                if(myarray[x,y].current_status == BURNT):
                    imgData[x,y] = (0,0,0)
                elif(myarray[x,y].current_status == SMOLDERING):
                    imgData[x,y] = (.75,.25,.25)
                else:
                    imgData[x,y] = (1,0,0)
            else:
                imgData[x,y] = mapVec[x,y][:-1]/255

    #    imgData = np.flip(imgData,0)
    fig = plt.figure(frameon=False)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    ax.xaxis.set_visible(False)
    ax.yaxis.set_visible(False)
    fig.add_axes(ax)
    ax.imshow(imgData)
    fig.savefig('imgs/example/frame_' + str(frameNumber) + '.png',bbox_inches='tight', pad_inches=0)
    

#class for each frame of game board
#each frame should be one pixel of map
class Frame:
    windspeed = 0
    humidity = 0
    elevation = 0
    biome = 0
    wind_direction = NE
    current_status = GREEN
    transition = False
    crowning = False
    conditions = None
    new_status = GREEN
    burn_count = 0





#Assuming we can get RGB values, this is how we determine the biome for each pixel.
def biome(RGB):
    if np.array_equal(RGB, [0, 0, 0]) or np.array_equal(RGB, [8, 155, 8]) or np.array_equal(RGB, [163,73,164]) :
        return WATER
    if np.array_equal(RGB,[255,93,100]) or np.array_equal(RGB,[238,28,36]) or np.array_equal(RGB,[237,32,40]) or np.array_equal(RGB,[237,28,36]) or np.array_equal(RGB,[234,0,8]):
        return SCRUB
    if np.array_equal(RGB, [0, 64, 26]) or np.array_equal(RGB, [3,4,4]) or np.array_equal(RGB,[34,177,76]) or np.array_equal(RGB,[63, 72, 204]) or np.array_equal(RGB,[36,185,79]):
        #print('coniferous')
        return CONIFEROUS
    if np.array_equal(RGB, [254, 244, 1]) or np.array_equal(RGB,[213,180,180]):
        return MONTANE
    if(np.array_equal(RGB,[63, 72, 204])):
        return CHAPARRAL
    #print(RGB)
    return MONTANE

#This is the dictionary of biome types, including their 4 associated variables.
#0. Difficulty to set on fire
#1. Scaling factor for windspeed
#2. Scaling factor for humidity
#3. Scaling factor for elevatio

def crowntransit(biome,windspeed=5,humidity=5,elevation=100):


    BIDICT = {
    WATER: (-1, 0, 0, 5), 
    SCRUB: (0.1, 1, -1, .5),
    MONTANE:(0.6,0.5,-3,1),
    CONIFEROUS:(0.4,0.5,-3,4),
    CHAPARRAL:(0.8,1,-2,1)
    }

    if((BIDICT[biome][0] + BIDICT[biome][1]* windspeed - BIDICT[biome][2]* humidity) >0):
        crowning = True
    else:
        crowning = False

    if((BIDICT[biome][0] - BIDICT[biome][3]* elevation + BIDICT[biome][1]* windspeed) >0):
        transiting = True
    else:
        transiting = False
    return (crowning, transiting)



#burns happen uphill

#algorithm determines T and C



#surface burn -slow fire : 


def set_board(game_board,biomeMap,heightMap,wind_direction=NE,humidity=0.5,elevation=100):
    new_board = np.empty(game_board.shape,dtype=object)


    for x in range(new_board.shape[0]):
        for y in range(new_board.shape[1]):    
            new_board[x,y] = Frame()
            new_board[x,y].greenness = game_board[x,y]
            new_board[x,y].wind_direction = wind_direction
            new_board[x,y].humidity = humidity
            new_board[x,y].elevation = heightMap[x,y][1]
            new_board[x,y].biome = biome(biomeMap[x,y])
            new_board[x,y].crowning, new_board[x,y].transition = crowntransit(new_board[x,y].biome,elevation=new_board[x,y].elevation)
            new_board[x,y].conditions = getConditions(new_board[x,y].crowning, new_board[x,y].transition)

    return new_board


def getConditions(crowning, transition):
    if(crowning and transition):
        return HIGH
    if(crowning and not transition):
        return MEDIUM
    if(not crowning and transition):
        return STOP
    if(not crowning and not transition):
        return LOW

def getBurn(greenpixel):
  # if greenpixel * random > 0
  if(random.randint(1,255) < greenpixel):
    return 1

  return 0

def canBurn(game_board,x_spot,y_spot):
    if(game_board.shape[0] <= x_spot  or
        game_board.shape[1] <= y_spot or
        x_spot < 0 or y_spot < 0):
        return 0
    if (game_board[x_spot,y_spot].biome >=5):
        return 1
    return 0


def spread(windspeed,delta_elevation, biome):
    if(biome == WATER):
        #print('Water')
        return False
    if(biome < 5):
        return False
    elif(biome == SCRUB):
        b = -0.2
    elif(biome == CONIFEROUS):
        b = 0
    elif(biome == MONTANE):
        b = 0.1
    elif(biome == CHAPARRAL):
        b = 0.2

    if(delta_elevation >0):
        e = 0.2
    elif(delta_elevation <0):
        e = -0.2
    else:
        e = 0
    probability = 0.5 + 0.1* windspeed + e + b
    if probability <0:
        return False
    else:
        x = random.randint(1, 100)
        if(x<= probability *100):
            return True
        else:
            return False

WIND_LOOKUP = {
    N : [0,1],
    S : [0,-1],
    W : [-1,0],
    E : [1,0]
}
def advance_board(game_board,wind_direction=NE,windspeed=2):
    #print('Dir',wind_direction,windspeed)
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
            if(game_board[x,y].current_status in burned):
                game_board[x,y].burn_count +=1
                if(game_board[x,y].current_status == BURNING):
                    # game_board[x,y].new_status = SMOLDERING

                    if(wind_direction == N):
                        if(game_board[x,y].conditions in [HIGH, MEDIUM, LOW]):
                            if(spread(game_board[x, y+1].windspeed, game_board[x, y].elevation - game_board[x, y+1].elevation, game_board[x, y+1].biome) and
                             (game_board[x, y+1].current_status not in burned)):
                                game_board[x, y+1].new_status = BURNING
                        if(game_board[x,y].conditions in [HIGH, MEDIUM]):
                            if(spread(game_board[x+1, y+1].windspeed, game_board[x, y].elevation - game_board[x+1, y+1].elevation, game_board[x+1, y+1].biome) and
                             (game_board[x+1, y+1].current_status not in burned)):
                                    game_board[x+1, y+1].new_status = BURNING
                            if(spread(game_board[x-1, y+1].windspeed, game_board[x, y].elevation - game_board[x-1, y+1].elevation, game_board[x-1, y+1].biome) and
                             (game_board[x-1, y+1].current_status not in burned)):
                                    game_board[x-1, y+1].new_status = BURNING
                        if(game_board[x,y].conditions is HIGH):
                            if(spread(game_board[x, y+2].windspeed, game_board[x, y].elevation - game_board[x, y+2].elevation, game_board[x, y+2].biome) and
                             (game_board[x, y+2].current_status not in burned)):
                                    game_board[x, y+2].new_status = BURNING
                            if(spread(game_board[x-1, y+2].windspeed, game_board[x, y].elevation - game_board[x-1, y+2].elevation, game_board[x-1, y+2].biome) and
                             (game_board[x-1, y+2].current_status not in burned)):
                                    game_board[x-1, y+2].new_status = BURNING
                            if(spread(game_board[x+1, y+2].windspeed, game_board[x, y].elevation - game_board[x+1, y+2].elevation, game_board[x+1, y+2].biome) and
                             (game_board[x+1, y+2].current_status not in burned)):
                                    game_board[x+1, y+2].new_status = BURNING

                    elif(wind_direction == NE):
                        if(game_board[x,y].conditions in [HIGH, MEDIUM, LOW]):
                            if(spread(game_board[x+1, y+1].windspeed, game_board[x, y].elevation - game_board[x+1, y+1].elevation, game_board[x+1, y+1].biome) and
                             (game_board[x+1, y+1].current_status not in burned)):
                                    game_board[x+1, y+1].new_status = BURNING
                        if(game_board[x,y].conditions in [HIGH, MEDIUM]):
                            if(spread(game_board[x, y+1].windspeed, game_board[x, y].elevation - game_board[x, y+1].elevation, game_board[x, y+1].biome) and
                             (game_board[x, y+1].current_status not in burned)):
                                    game_board[x, y+1].new_status = BURNING
                            if(spread(game_board[x+1, y].windspeed, game_board[x, y].elevation - game_board[x+1, y].elevation, game_board[x+1, y].biome) and
                             (game_board[x+1, y].current_status not in burned)):
                                    game_board[x+1, y].new_status = BURNING
                        if(game_board[x,y].conditions == HIGH):
                            if(spread(game_board[x+2, y+2].windspeed, game_board[x, y].elevation - game_board[x+2, y+2].elevation, game_board[x+2, y+2].biome) and
                             (game_board[x+2, y+2].current_status not in burned)):
                                    game_board[x+2, y+2].new_status = BURNING
                            if(spread(game_board[x, y+2].windspeed, game_board[x, y].elevation - game_board[x, y+2].elevation, game_board[x, y+2].biome) and
                             (game_board[x, y+2].current_status not in burned)):
                                    game_board[x, y+2].new_status = BURNING
                            if(spread(game_board[x+2, y].windspeed, game_board[x, y].elevation - game_board[x+2, y].elevation, game_board[x+2, y].biome) and
                             (game_board[x+2, y].current_status not in burned)):
                                    game_board[x+2, y].new_status = BURNING

                    elif(wind_direction == E):
                        if(game_board[x,y].conditions in [HIGH, MEDIUM, LOW]):
                            if(spread(game_board[x+1, y].windspeed, game_board[x, y].elevation - game_board[x+1, y].elevation, game_board[x+1, y].biome) and
                             (game_board[x+1, y].current_status not in burned)):
                                    game_board[x+1, y].new_status = BURNING
                        if(game_board[x,y].conditions in [HIGH, MEDIUM]):
                            if(spread(game_board[x+1, y+1].windspeed, game_board[x, y].elevation - game_board[x+1, y+1].elevation, game_board[x+1, y+1].biome) and
                             (game_board[x+1, y+1].current_status not in burned)):
                                    game_board[x+1, y+1].new_status = BURNING
                            if(spread(game_board[x+1, y-1].windspeed, game_board[x, y].elevation - game_board[x+1, y-1].elevation, game_board[x+1, y-1].biome) and
                             (game_board[x+1, y-1].current_status not in burned)):
                                    game_board[x+1, y-1].new_status = BURNING
                        if(game_board[x,y].conditions == HIGH):
                            if(spread(game_board[x+2, y+1].windspeed, game_board[x, y].elevation - game_board[x+2, y+1].elevation, game_board[x+2, y+1].biome) and
                             (game_board[x+2, y+1].current_status not in burned)):
                                    game_board[x+2, y+1].new_status = BURNING
                            if(spread(game_board[x+2, y-1].windspeed, game_board[x, y].elevation - game_board[x+2, y-1].elevation, game_board[x+2, y-1].biome) and
                             (game_board[x+2, y-1].current_status not in burned)):
                                    game_board[x+2, y-1].new_status = BURNING
                            if(spread(game_board[x+2, y].windspeed, game_board[x, y].elevation - game_board[x+2, y].elevation, game_board[x+2, y].biome) and
                             (game_board[x+2, y].current_status not in burned)):
                                    game_board[x+2, y].new_status = BURNING

                    elif(wind_direction == SE):
                        if(game_board[x,y].conditions in [HIGH, MEDIUM, LOW]):
                            if(spread(game_board[x+1, y-1].windspeed, game_board[x, y].elevation - game_board[x+1, y-1].elevation, game_board[x+1, y-1].biome) and
                             (game_board[x+1, y-1].current_status not in burned)):
                                    game_board[x+1, y-1].new_status = BURNING
                        if(game_board[x,y].conditions in [HIGH, MEDIUM]):
                            if(spread(game_board[x, y-1].windspeed, game_board[x, y-1].elevation - game_board[x, y-1].elevation, game_board[x, y-1].biome) and
                             (game_board[x, y-1].current_status not in burned)):
                                    game_board[x, y-1].new_status = BURNING
                            if(spread(game_board[x+1, y-1].windspeed, game_board[x, y].elevation - game_board[x+1, y-1].elevation, game_board[x+1, y-1].biome) and
                             (game_board[x+1, y-1].current_status not in burned)):
                                    game_board[x+1, y-1].new_status = BURNING
                        if(game_board[x,y].conditions == HIGH):
                            if(spread(game_board[x+2, y-2].windspeed, game_board[x, y].elevation - game_board[x+2, y-2].elevation, game_board[x+2, y-2].biome) and
                             (game_board[x+2, y-2].current_status not in burned)):
                                    game_board[x+2, y-2].new_status = BURNING
                            if(spread(game_board[x, y-2].windspeed, game_board[x, y].elevation - game_board[x, y-2].elevation, game_board[x, y-2].biome) and
                             (game_board[x, y-2].current_status not in burned)):
                                    game_board[x, y-2].new_status = BURNING
                            if(spread(game_board[x+2, y].windspeed, game_board[x, y].elevation - game_board[x+2, y].elevation, game_board[x+2, y].biome) and
                             (game_board[x+2, y].current_status not in burned)):
                                    game_board[x+2, y].new_status = BURNING                            


                    elif(wind_direction == S):
                        if(game_board[x,y].conditions in [HIGH, MEDIUM, LOW]):
                            if(spread(game_board[x, y-1].windspeed, game_board[x, y].elevation - game_board[x, y-1].elevation, game_board[x, y-1].biome) and
                             (game_board[x, y-1].current_status not in burned)):
                                    game_board[x, y-1].new_status = BURNING
                        if(game_board[x,y].conditions in [HIGH, MEDIUM]):
                            if(spread(game_board[x-1, y-1].windspeed, game_board[x, y].elevation - game_board[x-1, y-1].elevation, game_board[x-1, y-1].biome) and
                             (game_board[x-1, y-1].current_status not in burned)):
                                    game_board[x-1, y-1].new_status = BURNING
                            if(spread(game_board[x+1, y-1].windspeed, game_board[x, y].elevation - game_board[x+1, y-1].elevation, game_board[x+1, y-1].biome) and
                             (game_board[x+1, y-1].current_status not in burned)):
                                    game_board[x+1, y-1].new_status = BURNING
                        if(game_board[x,y].conditions == HIGH):
                            if(spread(game_board[x+1, y-2].windspeed, game_board[x, y].elevation - game_board[x+1, y-2].elevation, game_board[x+1, y-2].biome) and
                             (game_board[x+1, y-2].current_status not in burned)):
                                    game_board[x+1, y-2].new_status = BURNING
                            if(spread(game_board[x, y-2].windspeed, game_board[x, y].elevation - game_board[x, y-2].elevation, game_board[x, y-2].biome) and
                             (game_board[x, y-2].current_status not in burned)):
                                    game_board[x, y-2].new_status = BURNING
                            if(spread(game_board[x-1, y-2].windspeed, game_board[x, y].elevation - game_board[x-1, y-2].elevation, game_board[x-1, y-2].biome) and
                             (game_board[x-1, y-2].current_status not in burned)):
                                    game_board[x-1, y-2].new_status = BURNING 

                    elif(wind_direction == SW):
                        if(game_board[x,y].conditions in [HIGH, MEDIUM, LOW]):
                            if(spread(game_board[x-1, y-1].windspeed, game_board[x, y].elevation - game_board[x-1, y-1].elevation, game_board[x-1, y-1].biome) and
                             (game_board[x-1, y-1].current_status not in burned)):
                                    game_board[x-1, y-1].new_status = BURNING
                        if(game_board[x,y].conditions in [HIGH, MEDIUM]):
                            if(spread(game_board[x, y-1].windspeed, game_board[x, y].elevation - game_board[x, y-1].elevation, game_board[x, y-1].biome) and
                             (game_board[x, y-1].current_status not in burned)):
                                    game_board[x, y-1].new_status = BURNING
                            if(spread(game_board[x-1, y].windspeed, game_board[x, y].elevation - game_board[x-1, y].elevation, game_board[x-1, y].biome) and
                             (game_board[x-1, y].current_status not in burned)):
                                    game_board[x-1, y].new_status = BURNING
                        if(game_board[x,y].conditions == HIGH):
                            if(spread(game_board[x-2, y-2].windspeed, game_board[x, y].elevation - game_board[x-2, y-2].elevation, game_board[x-2, y-2].biome) and
                             (game_board[x-2, y-2].current_status not in burned)):
                                    game_board[x-2, y-2].new_status = BURNING
                            if(spread(game_board[x, y-2].windspeed, game_board[x, y].elevation - game_board[x, y-2].elevation, game_board[x, y-2].biome) and
                             (game_board[x, y-2].current_status not in burned)):
                                    game_board[x, y-2].new_status = BURNING
                            if(spread(game_board[x-2, y].windspeed, game_board[x, y].elevation - game_board[x-2, y].elevation, game_board[x-2, y].biome) and
                             (game_board[x-2, y].current_status not in burned)):
                                    game_board[x-2, y].new_status = BURNING 

                    elif(wind_direction == W):
                        if(game_board[x,y].conditions in [HIGH, MEDIUM, LOW]):
                            if(spread(game_board[x-1, y].windspeed, game_board[x, y].elevation - game_board[x-1, y].elevation, game_board[x-1, y].biome) and
                             (game_board[x-1, y].current_status not in burned)):
                                    game_board[x-1, y].new_status = BURNING
                        if(game_board[x,y].conditions in [HIGH, MEDIUM]):
                            if(spread(game_board[x-1, y-1].windspeed, game_board[x, y].elevation - game_board[x-1, y-1].elevation, game_board[x-1, y-1].biome) and
                             (game_board[x-1, y-1].current_status not in burned)):
                                    game_board[x-1, y-1].new_status = BURNING
                            if(spread(game_board[x-1, y+1].windspeed, game_board[x, y].elevation - game_board[x-1, y+1].elevation, game_board[x-1, y+1].biome) and
                             (game_board[x-1, y+1].current_status not in burned)):
                                    game_board[x-1, y+1].new_status = BURNING
                        if(game_board[x,y].conditions == HIGH):
                            if(spread(game_board[x-2, y-1].windspeed, game_board[x, y].elevation - game_board[x-2, y-1].elevation, game_board[x-2, y-1].biome) and
                             (game_board[x-2, y-1].current_status not in burned)):
                                    game_board[x-2, y-1].new_status = BURNING
                            if(spread(game_board[x-2, y+1].windspeed, game_board[x, y].elevation - game_board[x-2, y+1].elevation, game_board[x-2, y+1].biome) and
                             (game_board[x-2, y+1].current_status not in burned)):
                                    game_board[x-2, y+1].new_status = BURNING
                            if(spread(game_board[x-2, y].windspeed, game_board[x, y].elevation - game_board[x-2, y].elevation, game_board[x-2, y].biome) and
                             (game_board[x-2, y].current_status not in burned)):
                                    game_board[x-2, y].new_status = BURNING 

                    else: #NW
                        if(game_board[x,y].conditions in [HIGH, MEDIUM, LOW]):
                            if(spread(game_board[x-1, y+1].windspeed, game_board[x, y].elevation - game_board[x-1, y+1].elevation, game_board[x-1, y+1].biome) and
                             (game_board[x-1, y+1].current_status not in burned)):
                                    game_board[x-1, y+1].new_status = BURNING
                        if(game_board[x,y].conditions in [HIGH, MEDIUM]):
                            if(spread(game_board[x-1, y].windspeed, game_board[x, y].elevation - game_board[x-1, y].elevation, game_board[x-1, y].biome) and
                             (game_board[x-1, y].current_status not in burned)):
                                    game_board[x-1, y].new_status = BURNING
                            if(spread(game_board[x, y+1].windspeed, game_board[x, y].elevation - game_board[x, y+1].elevation, game_board[x, y+1].biome) and
                             (game_board[x, y+1].current_status not in burned)):
                                    game_board[x, y+1].new_status = BURNING
                        if(game_board[x,y].conditions == HIGH):
                            if(spread(game_board[x-2, y+2].windspeed, game_board[x, y].elevation - game_board[x-2, y+2].elevation, game_board[x-2, y+2].biome) and
                             (game_board[x-2, y+2].current_status not in burned)):
                                    game_board[x-2, y+2].new_status = BURNING
                            if(spread(game_board[x-2, y].windspeed, game_board[x, y].elevation - game_board[x-2, y].elevation, game_board[x-2, y].biome) and
                             (game_board[x-2, y].current_status not in burned)):
                                    game_board[x-2, y].new_status = BURNING
                            if(spread(game_board[x, y+2].windspeed, game_board[x, y].elevation - game_board[x, y+2].elevation, game_board[x, y+2].biome) and
                             (game_board[x, y+2].current_status not in burned)):
                                    game_board[x, y+2].new_status = BURNING 



                if(game_board[x,y].burn_count == 10):
                    game_board[x,y].new_status = SMOLDERING

                if(game_board[x,y].burn_count == 30):
                    game_board[x,y].new_status = BURNT
            
    
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
            game_board[x,y].current_status = game_board[x,y].new_status
    # return the new board
    return game_board




# In[41]:
def stepSimulation(game_board,frames,humidity,windspeed,winddir):
    if(frames > 0):
        #print('Wind direction',winddir)
        for x in range(5):
            game_board = advance_board(game_board,wind_direction=int(winddir),windspeed=int(windspeed))
        frames = frames + 1
        plotgrid(game_board,frames)
        return frames,game_board

def runSimulation(flashPoint,humidity,windspeed,winddir):
    # 
    prob_tree=0.6
    board_size = 50

    #
    fig = plt.figure(figsize=(10,10))

    # 
    game_board = set_board(burnable,biomeImg,heightImg)
    for x in [-1,0,1]:
        for y in [-1,0,1]:
            game_board[int(flashPoint['x'])+x,int(flashPoint['y'])+y].current_status = BURNING

    frames = 0
    # Use a lovely for loop instead of a while loop
    for i in range(1):
        for x in range(5):
            game_board = advance_board(game_board,wind_direction=int(winddir),windspeed=int(windspeed))
        #random.seed()
        #wind_direction= random.choice([N,S,W,E,NW,NE,SW,SE])
        # save the game board with the frame number
        frames = frames + 1
        plotgrid(game_board,frames)
    return frames,game_board
             









