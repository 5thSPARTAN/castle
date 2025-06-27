import sys
sys.path.append("../build/")

from game_env import GameEnv

import matplotlib.pyplot as plt
import numpy as np

def card_from_action_mask_index( action_mask_index ):
    match action_mask_index:
        case 0|1|25|26|27|28:
            return 0
        case 2|3|4|5|6|7|8|9|10|11|12|13:
            return 2
        case _:
            return int(action_mask_index - 11)



# precondition: action_list will lead to a battle
# post condition: outputs the card value not the action mask index
def determine_battle_winner( action_list ):
    largest_value = max(action_list)
    if largest_value > 21: # 21 is the equivalant of playing a 10 (highest non face card)
        if 15 in action_list:
            return 4
        if 14 in action_list:
            return 3
    return int(largest_value - 11)

def create_graph(winning_cards, 
                  game_length, 
                  total_wins, 
                  cards_played_by_winners_2d, 
                  cards_played_by_losers_3d,
                  cards_stolen_by_winners_2d,
                  cards_stolen_by_losers_3d,
                  game_number,
                  SPECIAL_TRACKING,
                  SPECIAL_TRACKING_STOLEN,
                  MODEL_NAME):

    fig, axs = plt.subplots(5,3, figsize=(20,20))

    # ROW 1 -----------------------------------------------------------------------------------------------------
    counts, bins, patches = axs[0][0].hist(winning_cards, align="left", bins=[x for x in range(2,15)], density=True)
    axs[0][0].set_title("Winning Cards")

    norm = plt.Normalize(min(counts), max(counts))

    for count, patch in zip(counts,patches):
        axs[0][0].text(
            patch.get_x() + patch.get_width()/2,
            count,
            f"{(count*100):.2f}%",
            fontsize=7,
            ha="center",
            va="bottom"
            )

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
            if( x >= 2 and x <=13):
                list_of_cards_played_by_winners.append(x)

    list_of_cards_played_by_losers = []
    for game in cards_played_by_losers_3d:
        for player in game:
            for x in player:
                if( x >= 2 and x <=13):
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

    for x, y in zip(x_values, clean_difference):
        axs[1][2].text(x, y , f'{y:.3f}%', ha='center', va='bottom', fontsize=8)
 
    # ROW 3 -----------------------------------------------------------------------------------------------------

    # clean data
    list_of_cards_stolen_by_winners = []
    for game in cards_stolen_by_winners_2d:
        for x in game:
            if( x >= 1 and x <=13):
                list_of_cards_stolen_by_winners.append(x)

    list_of_cards_stolen_by_losers = []
    for game in cards_stolen_by_losers_3d:
        for player in game:
            for x in player:
                if( x >= 1 and x <=13):
                    list_of_cards_stolen_by_losers.append(x)

    clean_winners = np.array(list_of_cards_stolen_by_winners)
    clean_losers = np.array(list_of_cards_stolen_by_losers)

    winner_percents = []
    loser_percents = []

    counts, bins, patches = axs[2][0].hist(clean_winners, align="left", bins=[x for x in range(1,15)], density=True)
    axs[2][0].set_title("Card's Stolen by Winners")

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

    counts, bins, patches = axs[2][1].hist(clean_losers, align="left", bins=[x for x in range(1,15)], density=True)
    axs[2][1].set_title("Card's Stolen by Losers")

    norm = plt.Normalize(min(counts), max(counts))
    cmap = plt.cm.coolwarm

    for count, patch in zip(counts,patches):
        axs[2][1].text(
            patch.get_x() + patch.get_width()/2,
            count,
            f"{(count*100):.2f}%",
            fontsize=7,
            ha="center",
            va="bottom"
            )
        patch.set_facecolor(cmap(norm(count)))

        loser_percents.append(count)


    x_values = [x for x in range(1,14)]
    clean_difference = np.array(winner_percents) - np.array(loser_percents)

    axs[2][2].bar(x_values, clean_difference)
    axs[2][2].set_title("Percent Difference Between\nWinning and Losing")

    for x, y in zip(x_values, clean_difference):
        axs[2][2].text(x, y , f'{y:.3f}%', ha='center', va='bottom', fontsize=8)

    # ROW 4 -----------------------------------------------------------------------------------------------------

    # clean data
    list_of_cards_played_by_winners = []
    for game in cards_played_by_winners_2d:
        count = 0
        for x in reversed(game):
            if count > SPECIAL_TRACKING:
                break
            if( x >= 2 and x <=13):
                list_of_cards_played_by_winners.append(x)
                count += 1
            

    list_of_cards_played_by_losers = []
    for game in cards_played_by_losers_3d:
        for player in game:
            count = 0
            for x in player:
                if count > SPECIAL_TRACKING:
                    break
                if( x >= 2 and x <=13):
                    list_of_cards_played_by_losers.append(x)
                    count += 1

    clean_winners = np.array(list_of_cards_played_by_winners)
    clean_losers = np.array(list_of_cards_played_by_losers)

    winner_percents = []
    loser_percents = []

    counts, bins, patches = axs[3][0].hist(clean_winners, align="left", bins=[x for x in range(2,15)], density=True)
    axs[3][0].set_title(f"Card's Played by Winners\nin Last {SPECIAL_TRACKING} Turns")

    norm = plt.Normalize(min(counts), max(counts))
    cmap = plt.cm.coolwarm

    for count, patch in zip(counts,patches):
        axs[3][0].text(
            patch.get_x() + patch.get_width()/2,
            count,
            f"{(count*100):.2f}%",
            fontsize=7,
            ha="center",
            va="bottom"
            )
        patch.set_facecolor(cmap(norm(count)))

        winner_percents.append(count)

    counts, bins, patches = axs[3][1].hist(clean_losers, align="left", bins=[x for x in range(2,15)], density=True)
    axs[3][1].set_title(f"Card's Played by Losers\nin Last {SPECIAL_TRACKING} Turns")

    norm = plt.Normalize(min(counts), max(counts))
    cmap = plt.cm.coolwarm

    for count, patch in zip(counts,patches):
        axs[3][1].text(
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

    axs[3][2].bar(x_values, clean_difference)
    axs[3][2].set_title(f"Percent Difference Between\nWinning Cards and Losing Cards\nOver Last {SPECIAL_TRACKING} Turns")

    for x, y in zip(x_values, clean_difference):
        axs[3][2].text(x, y , f'{y:.3f}%', ha='center', va='bottom', fontsize=8)

    # ROW 5 -----------------------------------------------------------------------------------------------------

    # clean data
    list_of_cards_stolen_by_winners = []
    for game in cards_stolen_by_winners_2d:
        count = 0
        for x in reversed(game):
            if count > SPECIAL_TRACKING_STOLEN:
                break
            if( x >= 1 and x <=13):
                list_of_cards_stolen_by_winners.append(x)
                count += 1
            

    list_of_cards_stolen_by_losers = []
    for game in cards_stolen_by_losers_3d:
        for player in game:
            count = 0
            for x in player:
                if count > SPECIAL_TRACKING_STOLEN:
                    break
                if( x >= 1 and x <=13):
                    list_of_cards_stolen_by_losers.append(x)
                    count += 1

    clean_winners = np.array(list_of_cards_stolen_by_winners)
    clean_losers = np.array(list_of_cards_stolen_by_losers)

    winner_percents = []
    loser_percents = []

    counts, bins, patches = axs[4][0].hist(clean_winners, align="left", bins=[x for x in range(1,15)], density=True)
    axs[4][0].set_title(f"Last {SPECIAL_TRACKING_STOLEN} Cards Stolen By Winners")

    norm = plt.Normalize(min(counts), max(counts))
    cmap = plt.cm.coolwarm

    for count, patch in zip(counts,patches):
        axs[4][0].text(
            patch.get_x() + patch.get_width()/2,
            count,
            f"{(count*100):.2f}%",
            fontsize=7,
            ha="center",
            va="bottom"
            )
        patch.set_facecolor(cmap(norm(count)))

        winner_percents.append(count)

    counts, bins, patches = axs[4][1].hist(clean_losers, align="left", bins=[x for x in range(1,15)], density=True)
    axs[4][1].set_title(f"Last {SPECIAL_TRACKING_STOLEN} Cards Stolen By Losers")

    norm = plt.Normalize(min(counts), max(counts))
    cmap = plt.cm.coolwarm

    for count, patch in zip(counts,patches):
        axs[4][1].text(
            patch.get_x() + patch.get_width()/2,
            count,
            f"{(count*100):.2f}%",
            fontsize=8,
            ha="center",
            va="bottom"
            )
        patch.set_facecolor(cmap(norm(count)))

        loser_percents.append(count)


    x_values = [x for x in range(1,14)]
    clean_difference = np.array(winner_percents) - np.array(loser_percents)

    axs[4][2].bar(x_values, clean_difference)
    axs[4][2].set_title(f"Percent Difference Between Winners and Losers")

    for x, y in zip(x_values, clean_difference):
        axs[4][2].text(x, y , f'{y:.3f}%', ha='center', va='bottom', fontsize=8)

    # -----------------------------------------------------------------------------------------------------------

    plt.tight_layout(pad=0.5)
    fig.savefig(f"../graphs/Basic_Info:_{MODEL_NAME}_{game_number}_TESTS.png", dpi=300)
    #plt.show()

def is_power_of_1000(n):
    while n >= 1000 and n % 1000 == 0:
        n //= 1000
    return n == 1

def basic_info_collector(model_0,
                         model_1,
                         model_2,
                         model_3,
                         NUMBER_OF_GAMES,
                         NUMBER_OF_PLAYERS,
                         STARTING_HEALTH,
                         MAX_HEALTH,
                         SPECIAL_TRACKING,
                         SPECIAL_TRACKING_STOLEN,
                         NAME
                         ):

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
            action_list = [ model_0(obs[0]), 
                            model_1(obs[1]),
                            model_2(obs[2]),
                            model_3(obs[3])
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

        # if is_power_of_1000(game_number + 1):
        #     print(f"{game_number + 1} games completed")
        #     create_graph(winning_cards, 
        #         game_length, 
        #         total_wins, 
        #         cards_played_by_winners_2d, 
        #         cards_played_by_losers_3d,
        #         cards_stolen_by_winners_2d,
        #         cards_stolen_by_losers_3d,
        #         game_number + 1,
        #         SPECIAL_TRACKING,
        #         SPECIAL_TRACKING_STOLEN,
        #         NAME)
    create_graph(winning_cards, 
                game_length, 
                total_wins, 
                cards_played_by_winners_2d, 
                cards_played_by_losers_3d,
                cards_stolen_by_winners_2d,
                cards_stolen_by_losers_3d,
                game_number + 1,
                SPECIAL_TRACKING,
                SPECIAL_TRACKING_STOLEN,
                NAME)