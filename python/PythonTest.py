from BasicModels import select_random_action, always_steal_random_selector, logical_action_selector_v1, logical_action_selector_v2
from BasicInfoCollector import basic_info_collector
from MLModels import castle_ml_model_v1, model_trainer, trained_ml_model

def main():
    NUMBER_OF_GAMES = 1000000
    NUMBER_OF_PLAYERS = 4
    STARTING_HEALTH = 5
    MAX_HEALTH = 7

    SPECIAL_TRACKING = 10
    SPECIAL_TRACKING_STOLEN = 1
    
    NUMBER_OF_TRAINING_GAMES = 50000


    # model_0 = model_1 = model_2 = model_3 = select_random_action
    # NAME = "4_RANDOM"
    # basic_info_collector(model_0,model_1,model_2,model_3,NUMBER_OF_GAMES,NUMBER_OF_PLAYERS,STARTING_HEALTH,MAX_HEALTH,SPECIAL_TRACKING,SPECIAL_TRACKING_STOLEN,NAME)

    # model_0 = model_1 = model_2 = model_3 = always_steal_random_selector
    # NAME = "4_ALWAYS_STEAL_RANDOM"
    # basic_info_collector(model_0,model_1,model_2,model_3,NUMBER_OF_GAMES,NUMBER_OF_PLAYERS,STARTING_HEALTH,MAX_HEALTH,SPECIAL_TRACKING,SPECIAL_TRACKING_STOLEN,NAME)

    # model_0 = model_1 = always_steal_random_selector
    # model_2 = model_3 = select_random_action
    # NAME = "2_ALWAYS_STEAL_RANDOM_2_RANDOM"
    # basic_info_collector(model_0,model_1,model_2,model_3,NUMBER_OF_GAMES,NUMBER_OF_PLAYERS,STARTING_HEALTH,MAX_HEALTH,SPECIAL_TRACKING,SPECIAL_TRACKING_STOLEN,NAME)

    # model_0 = model_1 = logical_action_selector_v1
    # model_2 = model_3 = select_random_action
    # NAME = "2_v1_LOGICAL_2_RANDOM"
    # basic_info_collector(model_0,model_1,model_2,model_3,NUMBER_OF_GAMES,NUMBER_OF_PLAYERS,STARTING_HEALTH,MAX_HEALTH,SPECIAL_TRACKING,SPECIAL_TRACKING_STOLEN,NAME)

    model_0 = logical_action_selector_v2
    model_1 = model_2 = model_3 = select_random_action
    NAME = "1_v2_LOGICAL_3_RANDOM"
    basic_info_collector(model_0,model_1,model_2,model_3,NUMBER_OF_GAMES,NUMBER_OF_PLAYERS,STARTING_HEALTH,MAX_HEALTH,SPECIAL_TRACKING,SPECIAL_TRACKING_STOLEN,NAME)

    MODEL_NAME = "RANDOM_TRAIN"
    policy = model_trainer(castle_ml_model_v1, select_random_action, select_random_action, select_random_action, MODEL_NAME, NUMBER_OF_TRAINING_GAMES, NUMBER_OF_PLAYERS, STARTING_HEALTH, MAX_HEALTH)
    model_0 = trained_ml_model(policy=policy, deterministic=False)
    model_1 = model_2 = model_3 = select_random_action
    NAME = "1_ML_MODEL_RANDOM_TRAIN_3_RANDOM"
    basic_info_collector(model_0,model_1,model_2,model_3,NUMBER_OF_GAMES,NUMBER_OF_PLAYERS,STARTING_HEALTH,MAX_HEALTH,SPECIAL_TRACKING,SPECIAL_TRACKING_STOLEN,NAME)

    MODEL_NAME = "LOGICAL_TRAIN"
    policy = model_trainer(castle_ml_model_v1, logical_action_selector_v2, logical_action_selector_v2, logical_action_selector_v2, MODEL_NAME, NUMBER_OF_TRAINING_GAMES, NUMBER_OF_PLAYERS, STARTING_HEALTH, MAX_HEALTH)
    model_0 = trained_ml_model(policy=policy, deterministic=False)
    model_1 = model_2 = model_3 = select_random_action
    NAME = "1_ML_MODEL_LOGICAL_TRAIN_3_RANDOM"
    basic_info_collector(model_0,model_1,model_2,model_3,NUMBER_OF_GAMES,NUMBER_OF_PLAYERS,STARTING_HEALTH,MAX_HEALTH,SPECIAL_TRACKING,SPECIAL_TRACKING_STOLEN,NAME)
    

    model_1 = model_2 = model_3 = logical_action_selector_v2
    NAME = "1_ML_MODEL_LOGICAL_TRAIN_3_LOGICAL"
    basic_info_collector(model_0,model_1,model_2,model_3,NUMBER_OF_GAMES,NUMBER_OF_PLAYERS,STARTING_HEALTH,MAX_HEALTH,SPECIAL_TRACKING,SPECIAL_TRACKING_STOLEN,NAME)



if __name__ == "__main__":
    main()

        