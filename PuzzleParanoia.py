import random
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import pickle
from matplotlib import style
import time

rows, cols = 3, 3
length = rows*cols


COMPLETION_REWARD = 10
MOVE_PENALTY = 1
NUMBER_EPISODES = 1
SHOW_EVERY = 3000
MOVES_PER_EPISODE = 25

epsilon = 0.9
EPS_DECAY = 0.9998

LEARNING_RATE = 0.1
DISCOUNT = 0.95

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

    def state(self):
        return tuple(self.tiles)


# Real code
# initialize qTable
qTable = {}
state = [0 for i in range(length)]


def initQTable(r):
    if len(r) == 1:
        state[-1] = r[0]
        qTable[tuple(state)] = [np.random.uniform(-5, 0) for i in range(4)]
        return

    for i in r:
        state[length - len(r)] = i
        newRange = list(r)
        newRange.remove(i)
        initQTable(newRange)


ran = [i for i in range(length)]
initQTable(ran)
print(len(qTable))

for i in range(NUMBER_EPISODES):

    # make puzzle
    puzzle = Puzzle()

    for j in range(MOVES_PER_EPISODE):
        # get state
        obs = puzzle.state()

        # decide to render or not

        # choose an action, based on epsilon
        action = np.random.randint(0, 4)

        # take the action
        puzzle.moveTile(action)

        # calculate reward
        if puzzle.tiles == [1, 2, 3, 4, 5, 6, 7, 8, 0]:
            reward = COMPLETION_REWARD
        else:
            reward = -MOVE_PENALTY

        # get state after taking action
        newObs = puzzle.state()
        maxFutureQ = np.max(qTable[newObs])
        currentQ = qTable[obs][action]

        # update q
        if reward == COMPLETION_REWARD:
            newQ = COMPLETION_REWARD
        else:
            newQ = (1 - LEARNING_RATE) * currentQ + \
                LEARNING_RATE * (reward + DISCOUNT * maxFutureQ)
        qTable[obs][action] = newQ

        # render

        # check if done
        # if done, break

        print(f'We are taking this: {action}')
        puzzle.printPuzzle()
        print("-------------------")

    # add the reward to the list of reward

    # epsilon decay

# average rewards

# plot rewards

# save qTable
