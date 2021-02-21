import random
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import pickle
from matplotlib import style
import time

rows, cols = 3, 3
length = rows*cols


COMPLETION_REWARD = 100
MOVE_PENALTY = 1
NUMBER_EPISODES = 50000
SHOW_EVERY = 5000
MOVES_PER_EPISODE = 750

epsilon = 0.75
EPS_DECAY = 0.9999

LEARNING_RATE = 0.15
DISCOUNT = 0.95

startQTable = "qTable-1613864179.pickle"

# Tile is a element in list puzzle,
# direction is one of the following: "down", "up", "left", "right"
# puzzle is a list of int with cols*rows elements


def checkSolvable(array):
    inversions = 0
    for i in range(length):
        for j in range(length):
            if array[j] > array[i]:
                inversions += 1
    if inversions % 2 == 1:
        return False
    else:
        return True


class Puzzle:
    def __init__(self):
        self.tiles = [0 for x in range(rows * cols)]
        for i in range(rows*cols):
            self.tiles[i] = i
        random.shuffle(self.tiles)

        while not checkSolvable(self.tiles):
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


if startQTable is None:
    ran = [i for i in range(length)]
    initQTable(ran)
else:
    with open(startQTable, "rb") as f:
        qTable = pickle.load(f)

episodeRewards = []
for i in range(NUMBER_EPISODES):

    # make puzzle
    puzzle = Puzzle()

    # render or not
    if i % SHOW_EVERY == 0:
        print(f"on #{i}, epsilon is {epsilon}")
        show = True
    else:
        show = False

    episodeReward = 0

    for j in range(MOVES_PER_EPISODE):
        # get state
        obs = puzzle.state()

        # choose an action, based on epsilon
        if np.random.random() > epsilon:
            action = np.argmax(qTable[obs])
        else:
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

        episodeReward += reward

        # check if done
        # if done, break
        if reward == COMPLETION_REWARD:
            print(f"We got a success on episode {i}")
            break

    if show:
        print('--------------')
        puzzle.printPuzzle()

    # add the reward to the list of reward
    episodeRewards.append(episodeReward)

    # epsilon decay
    epsilon *= EPS_DECAY

# average rewards
movingAvg = np.convolve(episodeRewards, np.ones(
    (SHOW_EVERY,))/SHOW_EVERY, mode='valid')

# plot rewards
plt.plot([i for i in range(len(movingAvg))], movingAvg)
plt.ylabel(f"Reward {SHOW_EVERY}ma")
plt.xlabel("episode #")
plt.show()

# save qTable
if startQTable == None:
    with open(f"qTable-{int(time.time())}.pickle", "wb") as f:
        pickle.dump(qTable, f)
else:
    with open(startQTable, "wb") as f:
        pickle.dump(qTable, f)
