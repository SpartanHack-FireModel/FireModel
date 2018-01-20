
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

def plotgrid(greenlayer,redlayer):
    
    # Create the pixel array
    combo = np.zeros((greenlayer.shape[0],greenlayer.shape[1],3))
    # Iterate over the green and red arrays and set the pixels accordingly.
    for x in range(greenlayer.shape[0]):
      for y in range(greenlayer.shape[1]):
        if(redlayer[x,y] == 0):
          combo[x,y] = (0,greenlayer[x,y],0)
        else:
          combo[x,y] = (redlayer[x,y],0,0)

    # display the pixel array
    plt.imshow(combo)
    #plt.imshow(redlayer)
    # 
    plt.ylim([0,greenlayer.shape[0]]) 
    plt.xlim([0,greenlayer.shape[1]])  #Defines the edges of our board

    # 
    plt.tick_params(axis='both', which='both',  #I believe this is stylistic editing
                    bottom='off', top='off', left='off', right='off',
                    labelbottom='off', labelleft='off')
    plt.pause(.01)
    
def getBurn(greenpixel):
  # if greenpixel * random > 0
  if(random.randint(1,255) < greenpixel):
    return 1

  return 0

def advance_board(greenlayer,redlayer):
    '''
    Advances the game board using the given rules.
    Input: the initial game board.
    Output: the advanced game board
    '''
    
    # create a new array that's just like the original one, but initially set to all zeros (i.e., totally empty)
    new_red = np.zeros_like(redlayer)
    new_green = np.zeros_like(greenlayer)

    # loop over each cell in the board and decide what to do.
    # You'll need two loops here, one nested inside the other.
    for x in range(greenlayer.shape[0]):
        for y in range(greenlayer.shape[1]):
            
            # Check for each pixel to equal to the pixel constants
            if(greenlayer[x,y] > 0):
              new_green[x,y] = greenlayer[x,y]
            if(redlayer[x,y] > 0):
              new_green[x,y] = 0
              new_red[x,y] = int(random.random() < .9)
              for xalt in [-1,0,1]:
                for yalt in [-1,0,1]:
                  if((
                    ((x + xalt) < greenlayer.shape[0]) and 
                    (x+xalt) > 0 and
                    ((y + yalt) < greenlayer.shape[1]) and
                    (y + yalt > 0) and
                    (getBurn(greenlayer[x+xalt,y+yalt])))):
                      new_red[x+xalt,y+yalt] = 1


            
    
            # Now that we're inside the loops we need to apply our rules
        
            # if the cell was empty last turn, it's still empty.
            # if it was on fire last turn, it's now empty.
            
    
            # now, if there is a tree in the cell, we have to decide what to do
            
                
                # initially make the cell a tree in the new board
                

                # If one of the neighboring cells was on fire last turn, 
                # this cell is now on fire!
                # (make sure you account for whether or not you're on the edge!)
                

    # return the new board
    return new_green,new_red






# In[41]:

# 
prob_tree=0.6
board_size = 50

#
fig = plt.figure(figsize=(10,10))

# 
redlayer = np.zeros(greenlayer.shape)
redlayer[0] = [1]*(len(greenlayer[0]))
# 
plotgrid(greenlayer,redlayer)

# 
on_fire = True

# Use a lovely for loop instead of a while loop
for i in range(100):

    # 
    board_size = 50
    greenlayer,redlayer = advance_board(greenlayer,redlayer)
    # 
    plotgrid(greenlayer,redlayer)
    time.sleep(0.05)  # 
    clear_output(wait=True)
    display(fig)
    fig.clear()

    # 


    # 


# 
plt.close()               









