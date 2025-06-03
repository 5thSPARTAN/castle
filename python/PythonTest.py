import sys
sys.path.append("../build")

import game_env
from collections import deque

env = game_env.GameEnv(4,5,7)
obs = env.reset()
lst =[0,0,0,0]
output = env.step(lst)


print(output[0][0].features)
print(output[0][0].actionMask)
