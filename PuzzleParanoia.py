import random
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import pickle
from matplotlib import style
import time

rows, cols = 3, 3
length = rows*cols


NUMBER_EPISODES = 1
SHOW_EVERY = 3000
MOVES_PER_EPISODE = 25

# Tile is a element in list puzzle,
# direction is one of the following: "down", "up", "left", "right"
# puzzle is a list of int with cols*rows elements
class Puzzle:
    def __init__(self):
        self.tiles = [0 for x in range(rows * cols)]
        for i in range(rows*cols):
            self.tiles[i] = i
        random.shuffle(self.tiles)

    def moveTile(self, direction):
        # find index
        zeroIndex = self.tiles.index(0)
        # if moving down
        if direction == 0: #down
            # Zero is not on the last rows
            if zeroIndex + cols < length:
                # switches 0 and the tile
                self.tiles[zeroIndex] = self.tiles[zeroIndex + cols]
                self.tiles[zeroIndex + cols] = 0

        # if moving up
        if direction == 1: #up
            if zeroIndex - cols >= 0:
            # switches 0 and the tile
                self.tiles[zeroIndex] = self.tiles[zeroIndex - cols]
                self.tiles[zeroIndex - cols] = 0

        # if moving left
        if direction == 2: #left
            if zeroIndex % cols != 0:
                # switches 0 and the tile
                self.tiles[zeroIndex] = self.tiles[zeroIndex - 1]
                self.tiles[zeroIndex - 1] = 0

        # if moving right
        if direction == 3: #right
            if zeroIndex % cols != cols - 1:
                # switches 0 and the tile
                self.tiles[zeroIndex] = self.tiles[zeroIndex + 1]
                self.tiles[zeroIndex + 1] = 0

    def printPuzzle(self):
        for i in range(rows):
            for j in range(cols):
                print(self.tiles[i*cols+j], end=" ")
            print()


############################################# Real code

## initialize qTable

for i in range(NUMBER_EPISODES):

    # make puzzle
    puzzle = Puzzle()
    
    for j in range(MOVES_PER_EPISODE):
        # decide to render or not

        # choose an action, based on epsilon
        action = np.random.randint(0, 4)

        # take the action
        puzzle.moveTile(action)

        ## calculate reward

        ## update q

        # render   

        ## check if done
            # if done, break
        
        print(f'We are taking this: {action}')
        puzzle.printPuzzle()
        print("-------------------")

    ## add the reward to the list of reward

    # epsilon decay

## averge rewards

## plot rewards

# save qTable