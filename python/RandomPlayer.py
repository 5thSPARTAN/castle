import random

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

