import gym
import sys
sys.path.append('/Users/haoranwang/opt/anaconda3/lib/python3.8/site-packages')

env = gym.make("MountainCar-v0")
env.reset()

done = False

while not done:
    action = 2
    new_state, reward, done, _ = env.step(action)
    env.render()

env.close()
