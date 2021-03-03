import itertools

import numpy as np
import pandas as pd
from src.data_pipeline import DataPipeline

data_pipeline = DataPipeline()
players_list = data_pipeline.valid_players
players_list['AVG'] = players_list['SCR'] / players_list['RATING']
players_list.sort_values(by='AVG', inplace=True, ascending=False, ignore_index=True)
players_list = players_list[:60]

actions = list(range(len(players_list)))
max_weight = 430

def mu_policy(Q, epsilon, nA, observation, actions):
    """
    A epsilon-greedy policy.
    Args:
        - Q(DataFrame): q-table.
        - nA (int): Total amount of actions.
    """
    action_List = list(set(actions).difference(set(observation)))
    # After observing current state, get the culmulative rewards based on different actions.
    action_values = Q.loc[str(observation), :]
    # Greedy (Use the actions that can get the maximum rewards)
    greedy_action = action_values.idxmax()
    probabilities = np.zeros(nA)

    for action in action_List:
        probabilities[action] = 1/len(action_List) * epsilon
    probabilities[greedy_action] += (1 - epsilon)

    return probabilities

def pi_policy(Q, observation):
    """
    Greedy policy, chose the optimal action every time.
    Args:
        - Q(DataFrame): q-table.
    """
    action_values = Q.loc[str(observation), :]
    # Optimal action.
    best_action = action_values.idxmax()
    return np.eye(len(action_values))[best_action]

def env_reward(action, knapsack):
    rewards = 0
    knapsack_ = knapsack + [action]
    knapsack_.sort()

    knapsack_w = np.sum([players_list['RATING'][i] for i in knapsack_])
    if knapsack_w > max_weight:
        rewards = -100
        done = True
    else:
        rewards = players_list['SCR'][action]
        done = False

    return rewards, knapsack_, done

def check_state(Q, knapsack, actions):
    """Check the knapsack status is in the q-table or not. If not, update to the table."""
    if str(knapsack) not in Q.index:
        # Append new state to q table.
        q_table_new = pd.Series([np.NAN]*len(actions), index=Q.columns, name=str(knapsack))
        for i in list(set(actions).difference(set(knapsack))):
            q_table_new[i] = 0
        return Q.append(q_table_new)
    else:
        return Q

def q_learning(actions, num_episodes, discount_factor=1.0, alpha=0.7, epsilon=0.2):
    nA = len(actions)

    Q = pd.DataFrame(columns=actions)


    for episode in range(1, num_episodes + 1):
        knapsack = []
        Q = check_state(Q=Q, knapsack=knapsack, actions=actions)
        action = np.random.choice(nA, p=mu_policy(Q, epsilon, nA, knapsack, actions))

        for t in itertools.count():
            reward, next_knapsack, done = env_reward(action, knapsack)
            Q = check_state(Q, next_knapsack, actions)

            next_action = np.random.choice(nA, p=mu_policy(Q, epsilon, nA, next_knapsack, actions))

            Q.loc[str(knapsack), action] = (
                Q.loc[str(knapsack), action]
                + alpha * (
                    reward
                    + discount_factor * Q.loc[str(next_knapsack), :].max()
                    - Q.loc[str(knapsack), action]
                )
            )

            if done:
                break

            # if t > 20:
            #     break

            knapsack = next_knapsack
            action = next_action
    return Q

def simulation(Q):
    actionsList = []
    knapsack = []
    nA = len(actions)

    action = np.random.choice(nA, p=pi_policy(Q, knapsack))

    for t in itertools.count():
        actionsList.append(action)
        reward, next_knapsack, done = env_reward(action, knapsack)
        next_action = np.random.choice(nA, p=pi_policy(Q, next_knapsack))
        if done:
            actionsList.pop()
            break
        else:
            action = next_action
            knapsack = next_knapsack

    return actionsList

Q = q_learning(actions, num_episodes=1000000, discount_factor=1.0, alpha=0.7, epsilon=0.2)
Q.to_csv('./Q.csv')
actionsList = simulation(Q)
print(actionsList)
print(players_list.iloc[actionsList])

print(np.sum(players_list.iloc[actionsList]['SCR']))