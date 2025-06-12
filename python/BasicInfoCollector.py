import sys
sys.path.append("../build/")

from game_env import GameEnv
from BasicInfoUtils import determine_battle_winner
from BasicInfoUtils import select_random_action
from BasicInfoUtils import card_from_action_mask_index
from BasicInfoUtils import create_graph


import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def is_power_of_10(n):
    while n >= 10 and n % 10 == 0:
        n //= 10
    return n == 1


def main():
    NUMBER_OF_GAMES = 1000000
    NUMBER_OF_PLAYERS = 4
    STARTING_HEALTH = 5
    MAX_HEALTH = 7

    SPECIAL_TRACKING = 10
    SPECIAL_TRACKING_STOLEN = 1


    env = GameEnv(NUMBER_OF_PLAYERS, STARTING_HEALTH, MAX_HEALTH)



    # want to track

    # ROW 1
    #   distribution of winning cards (single battle setting)
    winning_cards = [] # 1D array
    #   game length
    game_length = [] # 1D array
    #   winning percentage
    total_wins = [0,0,0,0]

    # ROW 2, 4
    #   distribution of cards played by winners and compare it to distribution of cards played by losers
    cards_played_by_losers_3d = [] # 3d array
    cards_played_by_winners_2d = [] # 2D array

    # ROW 3, 5
    #   distribution of cards stolen by winners and compare it to distribution of cards stolen by losers
    cards_stolen_by_losers_3d = []
    cards_stolen_by_winners_2d = []



    # collect data

    for game_number in range(NUMBER_OF_GAMES):

        player0_cards = []
        player1_cards = []
        player2_cards = []
        player3_cards = []

        player0_stolen = []
        player1_stolen = []
        player2_stolen = []
        player3_stolen = []

        turn_count = 0 

        obs = env.reset()
        game_end = False
        while game_end == False:
            action_list = [ select_random_action(obs[0].actionMask), 
                            select_random_action(obs[1].actionMask),
                            select_random_action(obs[2].actionMask),
                            select_random_action(obs[3].actionMask)
                            ]
            
            # determine what cards won battle
            if all(action <= 24 for action in action_list) and all(action >= 14 for action in action_list):
                winning_cards.append(determine_battle_winner(action_list))
            
            player0_cards.append(card_from_action_mask_index(action_list[0]))
            player1_cards.append(card_from_action_mask_index(action_list[1]))
            player2_cards.append(card_from_action_mask_index(action_list[2]))
            player3_cards.append(card_from_action_mask_index(action_list[3]))

            if action_list[0] >= 1 and action_list[0] <= 13: player0_stolen.append(action_list[0])
            if action_list[1] >= 1 and action_list[1] <= 13: player1_stolen.append(action_list[1])
            if action_list[2] >= 1 and action_list[2] <= 13: player2_stolen.append(action_list[2])
            if action_list[3] >= 1 and action_list[3] <= 13: player3_stolen.append(action_list[3])

            turn_count = turn_count + 1

            output = env.step(action_list)

            obs = output[0]
            rewards = output[1]
            game_end = output[2]

            if game_end:
                if rewards[0] == 1:
                    cards_played_by_winners_2d.append(player0_cards)
                    cards_stolen_by_winners_2d.append(player0_stolen)

                    cards_played_by_losers_3d.append([player1_cards,player2_cards,player3_cards])
                    cards_stolen_by_losers_3d.append([player1_stolen,player2_stolen,player3_stolen])

                    total_wins[0] += 1
                elif rewards[1] == 1:
                    cards_played_by_winners_2d.append(player1_cards)
                    cards_stolen_by_winners_2d.append(player1_stolen)

                    cards_played_by_losers_3d.append([player0_cards,player2_cards,player3_cards])
                    cards_stolen_by_losers_3d.append([player0_stolen,player2_stolen,player3_stolen])

                    total_wins[1] += 1
                elif rewards[2] == 1:
                    cards_played_by_winners_2d.append(player2_cards)
                    cards_stolen_by_winners_2d.append(player2_stolen)

                    cards_played_by_losers_3d.append([player0_cards,player1_cards,player3_cards])
                    cards_stolen_by_losers_3d.append([player0_stolen,player1_stolen,player3_stolen])

                    total_wins[2] += 1
                elif rewards[3] == 1:
                    cards_played_by_winners_2d.append(player3_cards)
                    cards_stolen_by_winners_2d.append(player3_stolen)

                    cards_played_by_losers_3d.append([player0_cards,player1_cards,player2_cards])
                    cards_stolen_by_losers_3d.append([player0_stolen,player1_stolen,player2_stolen])

                    total_wins[3] += 1
                # else:
                    # print("Something is happening")
                    # print(obs[0].features)
                    # print(obs[0].actionMask)
                    # print(rewards)
                    # print(game_end)
                
                game_length.append(turn_count)

        if is_power_of_10(game_number + 1):
            print(f"{game_number + 1} games completed")
            create_graph(winning_cards, 
                game_length, 
                total_wins, 
                cards_played_by_winners_2d, 
                cards_played_by_losers_3d,
                cards_stolen_by_winners_2d,
                cards_stolen_by_losers_3d,
                game_number + 1,
                SPECIAL_TRACKING,
                SPECIAL_TRACKING_STOLEN)
    # create_graph(winning_cards, 
    #     game_length, 
    #     total_wins, 
    #     cards_played_by_winners_2d, 
    #     cards_played_by_losers_3d,
    #     cards_stolen_by_winners_2d,
    #     cards_stolen_by_losers_3d,
    #     game_number + 1,
    #     SPECIAL_TRACKING,
    #     SPECIAL_TRACKING_STOLEN)

if __name__ == "__main__":
    main()



