import sys
sys.path.append("../build/")

from game_env import GameEnv
from RandomPlayer import select_random_action 

from collections import deque

NUMBER_OF_GAMES = 1000
NUMBER_OF_PLAYERS = 4
STARTING_HEALTH = 5
MAX_HEALTH = 7


env = GameEnv(NUMBER_OF_PLAYERS, STARTING_HEALTH, MAX_HEALTH)

everyone_dead = False

for game_number in range(NUMBER_OF_GAMES):
    obs = env.reset()
    game_end = False
    while game_end == False:
        action_list = [ select_random_action(obs[0].actionMask), 
                        select_random_action(obs[1].actionMask),
                        select_random_action(obs[2].actionMask),
                        select_random_action(obs[3].actionMask)
                        ]
        
        print(action_list)

        output = env.step(action_list)

        obs = output[0]
        rewards = output[1]
        game_end = output[2]

        print(obs[0].features)

        if game_end == True and rewards[0] == 0 and rewards[1] == 0 and rewards[2] == 0 and rewards[3] == 0:
            everyone_dead = True
            print("everyone Dead")
            print(rewards)
            print(game_end)
            break

    if everyone_dead:
        break



        