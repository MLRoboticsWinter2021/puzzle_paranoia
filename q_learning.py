import gym
import numpy as np

env = gym.make("MountainCar-v0")

LEARNING_RATE = 0.1
DISCOUNT = 0.95
EPISODES = 25000

SHOW_EVERY = 2000

DISCREATE_OS_SIZE = [20] * len(env.observation_space.high)
discreateOSWindowsSize = (env.observation_space.high -
                          env.observation_space.low) / DISCREATE_OS_SIZE

epsilon = 0.5
START_EPSILON_DECAY = 1
END_EPSILON_DECAY = EPISODES // 2

epsilonDecayValue = epsilon / (END_EPSILON_DECAY - START_EPSILON_DECAY)

qTable = np.random.uniform(
    low=-2, high=0, size=(DISCREATE_OS_SIZE + [env.action_space.n]))


def getDiscreateState(state):
    discreateState = (state - env.observation_space.low) / \
        discreateOSWindowsSize
    return tuple(discreateState.astype(np.int))


for episode in range(EPISODES):
    if episode % SHOW_EVERY == 0:
        print(episode)
        render = True
    else:
        render = False
    discreateState = getDiscreateState(env.reset())
    done = False

    while not done:
        if np.random.random() > epsilon:
            action = np.argmax(qTable[discreateState])
        else:
            action = np.random.randint(0, env.action_space.n)

        newState, reward, done, _ = env.step(action)
        newDiscreateState = getDiscreateState(newState)

        if render:
            env.render()

        if not done:
            maxFutureQ = np.max(qTable[newDiscreateState])
            currentQ = qTable[discreateState + (action, )]
            newQ = (1 - LEARNING_RATE) * currentQ + \
                LEARNING_RATE * (reward + DISCOUNT * maxFutureQ)
            qTable[discreateState + (action, )] = newQ
        elif newState[0] >= env.goal_position:
            qTable[discreateState + (action, )] = 0
            print(f"We made it on episode: {episode}")

        discreateState = newDiscreateState

    if END_EPSILON_DECAY >= episode >= START_EPSILON_DECAY:
        epsilon -= epsilonDecayValue

env.close()
