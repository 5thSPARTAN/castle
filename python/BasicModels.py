import random


def select_random_action( obs ):
    action_mask = obs.actionMask
    true_indicies = []
    for i in range(len(action_mask)):
        if action_mask[i] == True:
            true_indicies.append(i)

    if len(true_indicies):
        return random.choice(true_indicies)
    return -1

def always_steal_random_selector( obs ):
    action_mask = obs.actionMask

    true_indicies = []
    for i in range(len(action_mask)):
        if action_mask[i] == True:
            if i != 1:
                true_indicies.append(i)

    if len(true_indicies):
        return random.choice(true_indicies)
    return -1


# Just winning cards
def logical_action_selector_v1( obs ):
    action_mask = obs.actionMask

    true_indicies = []
    for i in range(len(action_mask)):
        if action_mask[i] == True:
            true_indicies.append(i)
    
    if len(true_indicies):
        steal_targets = []

        if action_mask[25]:
            steal_targets.append(25)
        if action_mask[26]:
            steal_targets.append(26)
        if action_mask[27]:
            steal_targets.append(27)
        if action_mask[28]:
            steal_targets.append(28)
        
        # Battle Options
        # 4
        if action_mask[15]:
            return 15
        if action_mask[24]:
            return 24
        if action_mask[14]:
            return 14
        if action_mask[21]:
            return 21
        if action_mask[23]:
            return 23
        if action_mask[20]:
            return 20
        if action_mask[22]:
            return 22
        if action_mask[19]:
            return 19
        if len(steal_targets):
            return random.choice(steal_targets)
        if action_mask[18]:
            return 18
        if action_mask[17]:
            return 17
        if action_mask[16]:
            return 16
        
        if action_mask[4]:
            return random.choice([4,1])
        if action_mask[13]:
            return random.choice([13,1])
        if action_mask[3]:
            return random.choice([3,1])
        if action_mask[10]:
            return random.choice([10,1])
        if action_mask[12]:
            return random.choice([12,1])
        if action_mask[9]:
            return random.choice([9,1])
        if action_mask[11]:
            return random.choice([11,1])
        if action_mask[8]:
            return random.choice([8,1])
        if action_mask[7]:
            return random.choice([7,1])
        if action_mask[6]:
            return random.choice([6,1])
        if action_mask[5]:
            return random.choice([5,1])
        if action_mask[2]:
            return random.choice([2,1])
        
        return 0
    return -1

# Just whole game winning cards
def logical_action_selector_v2( obs ):
    action_mask = obs.actionMask

    true_indicies = []
    for i in range(len(action_mask)):
        if action_mask[i] == True:
            true_indicies.append(i)
    
    if len(true_indicies):
        steal_targets = []

        if action_mask[25]:
            steal_targets.append(25)
        if action_mask[26]:
            steal_targets.append(26)
        if action_mask[27]:
            steal_targets.append(27)
        if action_mask[28]:
            steal_targets.append(28)
        
        # Battle Options
        # 4
        if action_mask[24]:
            return 24
        if action_mask[22]:
            return 22
        if action_mask[23]:
            return 23
        if action_mask[21]:
            return 21
        if len(steal_targets):
            return random.choice(steal_targets)
        if action_mask[20]:
            return 20
        if action_mask[14]:
            return 14
        # all 0.009%
        mini_list = []
        if action_mask[15]:
            mini_list.append(15)
        if action_mask[17]:
            mini_list.append(17)
        if action_mask[19]:
            mini_list.append(19)
        if len(mini_list):
            return random.choice(mini_list)
        # all 0.010%
        mini_list = []
        if action_mask[16]:
            mini_list.append(16)
        if action_mask[18]:
            mini_list.append(18)
        if len(mini_list):
            return random.choice(mini_list)
        
        
        if action_mask[13]:
            return 13
        if action_mask[12]:
            return 12
        if action_mask[11]:
            return 11
        if action_mask[10]:
            return 10
        if action_mask[4]:
            return 4
        if action_mask[2]:
            return 2
        if action_mask[1]:
            return 1
        
        
        return 0
    return -1