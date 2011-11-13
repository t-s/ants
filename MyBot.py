#!/usr/bin/env python
from ants import *
import logging
import sys
from filterClass import * 
import math
import psyco
import time
import copy

log = logging.StreamHandler(sys.stderr)
f1 = SingleLevelFilter(logging.DEBUG,True)
log.addFilter(f1)
logger = logging.getLogger("my.logger")
logger.addHandler(log)
logger.setLevel(logging.DEBUG)
moves = []
movesThisTurn = []
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
        pass
		# initialize data structures after learning the game settings
    
    # do turn is run once per turn
    # the ants class has the game state and is updated by the Ants.run method
    # it also has several helper methods to use
    def do_turn(self, ants):
		myMap = {}
		movesThisTurn = []
		myMap = copy.deepcopy(ants.map)
		for x,row in enumerate(myMap): 
			for y,cell in enumerate(row): 
				if(myMap[x][y] == -4): #water, give high score
					myMap[x][y] = 10000
				elif(myMap[x][y] == -3): #food, give low score
					myMap[x][y] = 0
				else:
					myMap[x][y] = 1
					minCell = 10000
					temp = 0
					for food in ants.food_list: # food is a tu
						temp = math.sqrt(math.pow((food[0] - x),2)+\
									 math.pow((food[1] - y),2))
						if(temp <= minCell):
							minCell = temp
					myMap[x][y] = minCell
		#copy over positions of ants to avoid collisions
		for a_row, a_col in ants.my_ants():
			movesThisTurn.append((a_row,a_col))	
	
		for a_row, a_col in ants.my_ants():
			minim = 1000
			move = ''
			if(len(moves) > 4):
				moves.pop(0)
			if((a_row+1) <= 60):
				if((a_row+1,a_col) not in moves):
					if((a_row+1,a_col) not in movesThisTurn):
						if(myMap[a_row+1][a_col] < minim):
							minim = myMap[a_row+1][a_col]
							move = 'S'
							moves.append((a_row+1,a_col))
							movesThisTurn.append((a_row+1,a_col))
			if((a_row-1) >= 0):
				if((a_row-1,a_col) not in moves):
					if((a_row-1,a_col) not in movesThisTurn):
						if(myMap[a_row-1][a_col] < minim):
							minim = myMap[a_row-1][a_col]
							move = 'N'
							moves.append((a_row-1,a_col))
							movesThisTurn.append((a_row-1,a_col))
			if((a_col+1) < 90):
				if((a_row,a_col+1) not in moves):
					if((a_row,a_col+1) not in movesThisTurn):
						if(myMap[a_row][a_col+1] < minim):
							minim = myMap[a_row][a_col+1]
							move = 'E'
							moves.append((a_row,a_col+1))
							movesThisTurn.append((a_row,a_col+1))
			if((a_col-1) >= 0):
				if((a_row,a_col-1) not in moves):
					if((a_row,a_col-1) not in movesThisTurn):
						if(myMap[a_row][a_col-1] < minim):
							minim = myMap[a_row][a_col-1]
							move = 'W'
							moves.append((a_row,a_col-1))
							movesThisTurn.append((a_row,a_col-1))
			#logger.error("Score at current position is " + str(myMap[a_row][a_col]))
			#if(move == 'S'):
			#	logger.error("Move is S")
			#	logger.error("Score at new position is " + str(myMap[a_row+1][a_col]))			
			#if(move == 'N'):
			#	logger.error("Move is N")
			#	logger.error("Score at new position is " + str(myMap[a_row-1][a_col]))			
			#if(move == 'E'):
			#	logger.error("Move is E")
			#	logger.error("Score at new position is " + str(myMap[a_row][a_col+1]))			
			#if(move == 'W'):
			#	logger.error("Move is W")
			#	logger.error("Score at new position is " + str(myMap[a_row][a_col-1]))			
			#logger.error("Score at N is " + str(myMap[a_row-1][a_col]))
			#logger.error("Score at S is " + str(myMap[a_row+1][a_col]))
			#logger.error("Score at E is " + str(myMap[a_row][a_col+1]))
			#logger.error("Score at W is " + str(myMap[a_row][a_col-1]))
			ants.issue_order((a_row,a_col,move))
			
 
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
