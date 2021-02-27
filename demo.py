import random
import numpy as np
import pickle
import time
import sys
import os
from sty import fg, bg, ef, rs

rows, cols = 3, 3
length = rows*cols

def checkSolvable(array):
    temparray = array[:]
    temparray.remove(0)
    inversions = 0
    for i in range(length-1):
        for j in range(i + 1, length-1, 1):
            if temparray[j] > temparray[i]:
                inversions += 1
    if inversions % 2 == 1:
        return False
    else:
        return True


class Puzzle:
    def __init__(self, tiles=[]):
        if not tiles:
            self.tiles = [0 for x in range(rows * cols)]
            for i in range(rows*cols):
                self.tiles[i] = i
            random.shuffle(self.tiles)

            while not checkSolvable(self.tiles):
                random.shuffle(self.tiles)
        else:
            self.tiles = tiles
        
    def moveTile(self, direction):
        # find index
        zeroIndex = self.tiles.index(0)
        # if moving down
        if direction == 0:  # down
            # Zero is not on the last rows
            if zeroIndex + cols < length:
                # switches 0 and the tile
                self.tiles[zeroIndex] = self.tiles[zeroIndex + cols]
                self.tiles[zeroIndex + cols] = 0

        # if moving up
        if direction == 1:  # up
            if zeroIndex - cols >= 0:
                # switches 0 and the tile
                self.tiles[zeroIndex] = self.tiles[zeroIndex - cols]
                self.tiles[zeroIndex - cols] = 0

        # if moving left
        if direction == 2:  # left
            if zeroIndex % cols != 0:
                # switches 0 and the tile
                self.tiles[zeroIndex] = self.tiles[zeroIndex - 1]
                self.tiles[zeroIndex - 1] = 0

        # if moving right
        if direction == 3:  # right
            if zeroIndex % cols != cols - 1:
                # switches 0 and the tile
                self.tiles[zeroIndex] = self.tiles[zeroIndex + 1]
                self.tiles[zeroIndex + 1] = 0

    def printPuzzle(self):
        for i in range(rows):
            for j in range(cols):
                print(self.tiles[i*cols+j], end=" ")
            print()

    def toString(self):
        out = ""
        for i in range(rows):
            for j in range(cols):
                if not self.tiles[i*cols+j]:
                    out += fg(10, 204, 102)
                out += str(self.tiles[i*cols+j])
                if not self.tiles[i*cols+j]:
                    out += fg.rs
                out += " "
            out += "\n"
        return out

    def state(self):
        return tuple(self.tiles)


# input
tiles = input("Enter 9 unique numbers (0 - 8): ").split(" ")
for i in range(0, len(tiles)): 
    tiles[i] = int(tiles[i])

while not checkSolvable(tiles):
    print("Please enter again")
    tiles = input("Enter 9 unique numbers (0 - 8): ").split(" ")
    for i in range(0, len(tiles)): 
        tiles[i] = int(tiles[i])
    
puzzle = Puzzle(tiles)

# throw it in the algorithm
# get q table
qTable = {}
with open("qTable-1613866966.pickle", "rb") as f:
    qTable = pickle.load(f)

actions = []
states = []
for i in range(200):
    # get state
    obs = puzzle.state()

    # choose an action, based on epsilon
    action = np.argmax(qTable[obs])

    # take the action
    puzzle.moveTile(action)

    # record action and states
    actions.append(action)
    states.append(puzzle.toString())

    # check if done
    # if done, break
    if puzzle.tiles == [1, 2, 3, 4, 5, 6, 7, 8, 0]:
        break

# do animation
for j in range(len(actions)):
    ac = actions[j]
    actionString = ""
    if ac == 0:
        actionString = "down"
    elif ac == 1:
        actionString = "up"
    elif ac == 2:
        actionString = "left"
    else:
        actionString = "right"
    
    sys.stdout.write("We are moving the blank space (the 0 tile) " + actionString + "\n")

    if j == len(actions) - 1:
        sys.stdout.write(fg.blue + states[j] + fg.rs)
    else:
        sys.stdout.write(states[j])
    time.sleep(0.5)
    if not j == len(actions) - 1:
        os.system('clear')

