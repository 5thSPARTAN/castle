import sys
sys.path.append("../build/")

from game_env import GameEnv

import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim


class castle_ml_model_v1(nn.Module):
    def __init__(self, features_dim, action_mask_dim):
        super().__init__()
        self.fc1 = nn.Linear(features_dim, 64)
        self.fc2 = nn.Linear(64, 64)
        self.fc3 = nn.Linear(64, action_mask_dim)

    def forward(self, features, action_mask):
        x = F.relu(self.fc1(features))
        x = F.relu(self.fc2(x))
        logits = self.fc3(x)

        logits = logits.masked_fill(action_mask == 0, float('-inf'))

        action_probability = F.softmax(logits, dim=-1)
        return action_probability

def compute_returns(rewards, gamma):
    returns = []
    G = 0
    for r in reversed(rewards):
        G = r + gamma * G
        returns.insert(0, G)
    return torch.tensor(returns)

def model_trainer(training_model, 
                  model_1, 
                  model_2, 
                  model_3, 
                  MODEL_NAME,
                  NUMBER_OF_TRAINING_GAMES,
                  NUMBER_OF_PLAYERS,
                  STARTING_HEALTH,
                  MAX_HEALTH
                  ):
    total = 0
    n = 0
    env = GameEnv(NUMBER_OF_PLAYERS, STARTING_HEALTH, MAX_HEALTH)

    policy = training_model(features_dim=23, action_mask_dim=29)
    optimizer = optim.Adam(policy.parameters(), lr=1e-5)
    gamma = 0.9

    #training loop
    for episode in range(NUMBER_OF_TRAINING_GAMES):
        obs = env.reset()
        log_probs = []
        rewards = []

        done = False

        while not done:
            features_tensor = torch.tensor(obs[0].features, dtype=torch.float32).unsqueeze(0) # converts features to a torch type and adds dimention
            mask_tensor = torch.tensor(obs[0].actionMask, dtype=torch.bool).unsqueeze(0) # converts action mask to torch type and adds dimention

            action_probabilities = policy(features_tensor, mask_tensor).squeeze() #executes forward in the policy; needs the extra dimention to execute; gets rid of extra dimention after
            dist = torch.distributions.Categorical(action_probabilities) # creates Categorial class to call sample() from
            action = dist.sample()
            log_prob = dist.log_prob(action) # logarithm of the probablility to calculate loss with later
            
            action_list = [ action.item(), 
                            model_1(obs[1]),
                            model_2(obs[2]),
                            model_3(obs[3])
                            ]

            output = env.step(action_list) # item() turns tensor to int

            obs = output[0]
            reward = output[1]
            done = output[2]

            log_probs.append(log_prob)
            rewards.append(reward[0])
        
        returns = compute_returns(rewards, gamma) # adjusts all the returns over how every many rounds a game was

        loss = -torch.sum(torch.stack(log_probs) * returns) # loss function for REINFORCE

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()


        n += 1
        total += sum(rewards)
        if episode % 100 == 0:
            print(f"Episode {episode}, average reward: {total/n}")
            
            
    torch.save(policy.state_dict(), f"../models/{MODEL_NAME}_{NUMBER_OF_TRAINING_GAMES}.pt")
    return policy

def select_action(policy, features, action_mask, deterministic=False):
    policy.eval()
    
    with torch.no_grad():
        features_tensor = torch.tensor(features, dtype=torch.float32).unsqueeze(0)
        mask_tensor = torch.tensor(action_mask, dtype=torch.bool).unsqueeze(0)

        action_probabilities = policy(features_tensor, mask_tensor).squeeze(0)

        if deterministic:
            chosen_action = torch.argmax(action_probabilities).item()
        else:
            dist = torch.distributions.Categorical(action_probabilities)
            chosen_action = dist.sample().item()

    return chosen_action

class trained_ml_model(nn.Module):
    def __init__(self, policy, deterministic=False):
        super().__init__()
        self.policy = policy
        self.deterministic = deterministic

    def forward(self, obs ):
        return select_action(self.policy, obs.features, obs.actionMask, self.deterministic)