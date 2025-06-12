import sys
sys.path.append("../build/")

from game_env import GameEnv
from RandomPlayer import select_random_action
from RandomPlayer import determine_battle_winner
from RandomPlayer import card_from_action_mask_index

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

NUMBER_OF_GAMES = 10
NUMBER_OF_PLAYERS = 4
STARTING_HEALTH = 5
MAX_HEALTH = 7

SPECIAL_TRACKING = 5


env = GameEnv(NUMBER_OF_PLAYERS, STARTING_HEALTH, MAX_HEALTH)



# want to track

# ROW 1
#   distribution of winning cards (single battle setting)
winning_cards = [] # 1D array
#   game length
game_length = [] # 1D array
#   winning percentage
total_wins = [0,0,0,0]

#   distribution of cards played by winners and compare it to distribution of cards played by losers (over the game)
cards_played_by_losers_3d = [] # 3d array
cards_played_by_winners_2d = [] # 2D array



# collect data

for game_number in range(NUMBER_OF_GAMES):

    if ( game_number + 1) % 100 == 0:
        print(f"{game_number + 1} games completed")

    player0_cards = []
    player1_cards = []
    player2_cards = []
    player3_cards = []

    turn_count = 0 

    obs = env.reset()
    game_end = False
    while game_end == False:
        action_list = [ select_random_action(obs[0].actionMask), 
                        select_random_action(obs[1].actionMask),
                        select_random_action(obs[2].actionMask),
                        select_random_action(obs[3].actionMask)
                        ]
        
        if all(action <= 24 for action in action_list) and all(action >= 14 for action in action_list):
            winning_cards.append(determine_battle_winner(action_list))
        
        player0_cards.append(card_from_action_mask_index(action_list[0]))
        player1_cards.append(card_from_action_mask_index(action_list[1]))
        player2_cards.append(card_from_action_mask_index(action_list[2]))
        player3_cards.append(card_from_action_mask_index(action_list[3]))

        turn_count = turn_count + 1

        output = env.step(action_list)

        obs = output[0]
        rewards = output[1]
        game_end = output[2]

        if game_end:
            if rewards[0] == 1:
                cards_played_by_winners_2d.append(player0_cards)
                cards_played_by_losers_3d.append([player1_cards,player2_cards,player3_cards])
                total_wins[0] += 1
            elif rewards[1] == 1:
                cards_played_by_winners_2d.append(player1_cards)
                cards_played_by_losers_3d.append([player0_cards,player2_cards,player3_cards])
                total_wins[1] += 1
            elif rewards[2] == 1:
                cards_played_by_winners_2d.append(player2_cards)
                cards_played_by_losers_3d.append([player0_cards,player1_cards,player3_cards])
                total_wins[2] += 1
            elif rewards[3] == 1:
                cards_played_by_winners_2d.append(player3_cards)
                cards_played_by_losers_3d.append([player0_cards,player1_cards,player2_cards])
                total_wins[3] += 1
            # else:
                # print("Something is happening")
                # print(obs[0].features)
                # print(obs[0].actionMask)
                # print(rewards)
                # print(game_end)
            
            game_length.append(turn_count)





# create graphs

fig, axs = plt.subplots(3,3, figsize=(16,9))

# ROW 1 -----------------------------------------------------------------------------------------------------
axs[0][0].hist(winning_cards, bins=[x for x in range(2,14)])
axs[0][0].set_title("Winning Cards")

axs[0][1].hist(game_length, bins=[x for x in range(1,max(game_length))])
axs[0][1].set_title("Game Length")

axs[0][2].bar(["Player 1", "Player 2", "Player 3", "Player 4"], total_wins)
axs[0][2].set_title("Win Rate Per Player")

for i, value in enumerate(total_wins):
    axs[0][2].text(i, 
    value+0.5,
    f"{(value/sum(total_wins) * 100):.2f}%",
    ha="center",
    va="bottom"
    )

# ROW 2 -----------------------------------------------------------------------------------------------------

# clean data
list_of_cards_played_by_winners = []
for game in cards_played_by_winners_2d:
    for x in game:
        if( x >= 2 and x <=14):
            list_of_cards_played_by_winners.append(x)

list_of_cards_played_by_losers = []
for game in cards_played_by_losers_3d:
    for player in game:
        for x in player:
            if( x >= 2 and x <=14):
                list_of_cards_played_by_losers.append(x)

clean_winners = np.array(list_of_cards_played_by_winners)
clean_losers = np.array(list_of_cards_played_by_losers)

winner_percents = []
loser_percents = []

counts, bins, patches = axs[1][0].hist(clean_winners, align="left", bins=[x for x in range(2,15)], density=True)
axs[1][0].set_title("Card's Played by Winners")

norm = plt.Normalize(min(counts), max(counts))
cmap = plt.cm.coolwarm

for count, patch in zip(counts,patches):
    axs[1][0].text(
        patch.get_x() + patch.get_width()/2,
        count,
        f"{(count*100):.2f}%",
        fontsize=7,
        ha="center",
        va="bottom"
        )
    patch.set_facecolor(cmap(norm(count)))

    winner_percents.append(count)

counts, bins, patches = axs[1][1].hist(clean_losers, align="left", bins=[x for x in range(2,15)], density=True)
axs[1][1].set_title("Card's Played by Losers")

norm = plt.Normalize(min(counts), max(counts))
cmap = plt.cm.coolwarm

for count, patch in zip(counts,patches):
    axs[1][1].text(
        patch.get_x() + patch.get_width()/2,
        count,
        f"{(count*100):.2f}%",
        fontsize=7,
        ha="center",
        va="bottom"
        )
    patch.set_facecolor(cmap(norm(count)))

    loser_percents.append(count)


x_values = [x for x in range(2,14)]
clean_difference = np.array(winner_percents) - np.array(loser_percents)

axs[1][2].bar(x_values, clean_difference)
axs[1][2].set_title("Percent Difference Between\nWinning Cards and Losing Cards")

# ROW 3 -----------------------------------------------------------------------------------------------------

# clean data
list_of_cards_played_by_winners = []
for game in cards_played_by_winners_2d:
    count = 0
    for x in reversed(game):
        if count > SPECIAL_TRACKING:
            break
        if( x >= 2 and x <=14):
            list_of_cards_played_by_winners.append(x)
            count += 1
        

list_of_cards_played_by_losers = []
for game in cards_played_by_losers_3d:
    for player in game:
        count = 0
        for x in player:
            if count > SPECIAL_TRACKING:
                break
            if( x >= 2 and x <=14):
                list_of_cards_played_by_losers.append(x)
                count += 1

clean_winners = np.array(list_of_cards_played_by_winners)
clean_losers = np.array(list_of_cards_played_by_losers)

winner_percents = []
loser_percents = []

counts, bins, patches = axs[2][0].hist(clean_winners, align="left", bins=[x for x in range(2,15)], density=True)
axs[2][0].set_title(f"Card's Played by Winners\nin Last {SPECIAL_TRACKING} Turns")

norm = plt.Normalize(min(counts), max(counts))
cmap = plt.cm.coolwarm

for count, patch in zip(counts,patches):
    axs[2][0].text(
        patch.get_x() + patch.get_width()/2,
        count,
        f"{(count*100):.2f}%",
        fontsize=7,
        ha="center",
        va="bottom"
        )
    patch.set_facecolor(cmap(norm(count)))

    winner_percents.append(count)

counts, bins, patches = axs[2][1].hist(clean_losers, align="left", bins=[x for x in range(2,15)], density=True)
axs[2][1].set_title(f"Card's Played by Losers\nin Last {SPECIAL_TRACKING} Turns")

norm = plt.Normalize(min(counts), max(counts))
cmap = plt.cm.coolwarm

for count, patch in zip(counts,patches):
    axs[2][1].text(
        patch.get_x() + patch.get_width()/2,
        count,
        f"{(count*100):.2f}%",
        fontsize=8,
        ha="center",
        va="bottom"
        )
    patch.set_facecolor(cmap(norm(count)))

    loser_percents.append(count)


x_values = [x for x in range(2,14)]
clean_difference = np.array(winner_percents) - np.array(loser_percents)

axs[2][2].bar(x_values, clean_difference)
axs[2][2].set_title(f"Percent Difference Between\nWinning Cards and Losing Cards\nOver Last {SPECIAL_TRACKING} Turns")

plt.tight_layout()
fig.savefig(f"../graphs/Basic_Info:_{NUMBER_OF_GAMES}_TESTS_{SPECIAL_TRACKING}_SPECIAL.png", dpi=300)

plt.show()

# print(len(cards_played_by_winners_2d))
# print(len(cards_played_by_losers_3d))
# print(len(game_length))

# # winning_cards_df = pd.DataFrame(winning_cards)
# # winning_cards_df.to_csv("./csv/winning_cards.csv", index = False, header=False)

# cards_played_by_winners_df = pd.DataFrame(cards_played_by_winners)
# cards_played_by_winners_df.to_csv("./csv/cards_played_by_winners", index = False,header=False)

# game_length_df = pd.DataFrame(game_length)
# game_length_df.to_csv("./csv/game_length", index = False,header=False)

