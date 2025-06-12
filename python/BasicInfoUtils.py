import random
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def select_random_action( action_mask ):
    true_indicies = []
    for i in range(len(action_mask)):
        if action_mask[i] == True:
            true_indicies.append(i)

    if len(true_indicies):
        return random.choice(true_indicies)
    return -1

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
                  game_number,
                  SPECIAL_TRACKING):

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
    fig.savefig(f"../graphs/Basic_Info:_{game_number}_TESTS_{SPECIAL_TRACKING}_SPECIAL.png", dpi=300)