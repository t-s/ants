#!/usr/bin/env python
from ants import *
import logging
import sys
from filterClass import * 
import math

log = logging.StreamHandler(sys.stderr)
f1 = SingleLevelFilter(logging.DEBUG,True)
log.addFilter(f1)
logger = logging.getLogger("my.logger")
logger.addHandler(log)
logger.setLevel(logging.DEBUG)


# define a class with a do_turn method
# the Ants.run method will parse and update bot input
# it will also run the do_turn method for us
class MyBot:
    def __init__(self):
        # define class level variables, will be remembered between turns
        pass
    # do_setup is run once at the start of the game
    # after the bot has received the game settings
    # the ants class is created and setup by the Ants.run method
    def do_setup(self, ants):
        # initialize data structures after learning the game settings
        pass
    
    # do turn is run once per turn
    # the ants class has the game state and is updated by the Ants.run method
    # it also has several helper methods to use
    def do_turn(self, ants):
        myMap = ants.map
        foodMap = ants.map
        exploreMap = ants.map
        lastSeenMap = ants.map
        diffuseExploreMap = []
        diffuseFoodMap = []
        goalsToDiffuse = []
        # enumerate returns index,item - in that order
        # for each row in copied over game map
        for rowPos,row in enumerate(myMap): 
        # for each column in row of game map
            for colPos,cell in enumerate(row):
                # if cell is water
                if (cell == -4):
                    # don't ever go there, sister
                    exploreMap[rowPos][colPos] = 0
                    # no food there
                    foodMap[rowPos][colPos] = 0
                    continue
                # if cell is food
                if (cell == -3):
                    # there's food here, arbitrarily high score in food map
                    foodMap[rowPos][colPos] = 10000
                else:
                    # if no food, we'll diffuse food values over this cell
                    #diffTup = (rowPos,colPos)
                    #diffuseFoodMap.append(diffTup)
                    goalsToDiffuse.append('food')
                    # if cell is unseen
                if (cell == -5):
                    # add to to be explored map, with factor value depending on time
                    # cell was last seen using last seen map
                    exploreMap[rowPos][colPos] = 10000 - \
                        ((200 - lastSeenMap[rowPos][colPos]) * 300)
                else:
                    # if cell has been explored and is seen, diffuse unseen values
                    # over this cell instead
                    #diffTup = (rowPos,colPos)
                    #diffuseExploreMap.append(diffTup)
                    goalsToDiffuse.append('explore')
       

        # loop through all my ants and try to give them orders
        # the ant_loc is an ant location tuple in (row, col) form
        for a_row, a_col in ants.my_ants():
            f = ants.closest_food(a_row,a_col)
            if (ants.passable(f[0],f[1])):
                direc = ants.direction(a_row, a_col, f[0], f[1])
                ants.issue_order((a_row, a_col, direc[0]))
            else:
                direc = ants.direction(a_row, a_col, f[0], f[1])
                ants.issue_order((a_row, a_col, direc[1]))
            break
            
if __name__ == '__main__':
    # psyco will speed up python a little, but is not needed
    try:
        import psyco
        psyco.full()
    except ImportError:
        pass
    
    try:
        # if run is passed a class with a do_turn method, it will do the work
        # this is not needed, in which case you will need to write your own
        # parsing function and your own game state class
        Ants.run(MyBot())
    except KeyboardInterrupt:
        print('ctrl-c, leaving ...')
