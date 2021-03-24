import heapq

import numpy as np
import pandas as pd
from src.data_pipeline import DataPipeline
from src.scrape import load_configs

MAXIMUM_SIZE = 3
score_heapq = []
name_dict = {}
name_set = set()

def recommand(valid_players):

    guards = valid_players[(valid_players.POSITION == "G") | (valid_players.POSITION == "F-G")]
    forwards = valid_players[
        (valid_players.POSITION == "F")
        | (valid_players.POSITION == "F-G")
        | (valid_players.POSITION == "C-F")
    ]
    centers = valid_players[(valid_players.POSITION == "C") | (valid_players.POSITION == "C-F")]

    guard_list = guards.to_numpy()
    forward_list = forwards.to_numpy()
    center_list = centers.to_numpy()

    def player_1():
        for idx1 in range(len(guard_list)):
            player_2(idx1)

    def player_2(idx1):
        for idx2 in range(idx1+1, len(guard_list)):
            if len({guard_list[idx1][0], guard_list[idx2][0]}) == 2:
                player_3(idx1, idx2)

    def player_3(idx1, idx2):
        for idx3 in range(len(forward_list)):
            if len({guard_list[idx1][0], guard_list[idx2][0], forward_list[idx3][0]}) == 3:
                player_4(idx1, idx2, idx3)

    def player_4(idx1, idx2, idx3):
        for idx4 in range(idx3+1, len(forward_list)):
            if len({guard_list[idx1][0], guard_list[idx2][0], forward_list[idx3][0], forward_list[idx4][0]}) == 4:
                player_5(idx1, idx2, idx3, idx4)

    def player_5(idx1, idx2, idx3, idx4):
        for idx5 in range(len(center_list)):
            player1 = guard_list[idx1]
            player2 = guard_list[idx2]
            player3 = forward_list[idx3]
            player4 = forward_list[idx4]
            player5 = center_list[idx5]

            player_list = [player1, player2, player3, player4, player5]
            # Players' name list.
            name_list = [player[0] for player in player_list]
            name_list.sort()
            # Combine them as a string.
            names = '-'.join(name_list)
            # Players' rating list.
            rating_list = [player[3] for player in player_list]
            total_rating = sum(rating_list)
            # Players' score list.
            score_list = [player[-2] for player in player_list]
            total_score = sum(score_list)

            if (len(set(name_list)) == 5) and (total_rating <= 430) and (names not in name_set) and (
                len(score_heapq) < MAXIMUM_SIZE or (total_score >= score_heapq[0])
            ):
                # Maintain a fixed size heapq.
                if len(score_heapq) >= MAXIMUM_SIZE:
                    heapq.heappop(score_heapq)

                res = total_score
                heapq.heappush(score_heapq, res)
                name_set.add(names)

                choice = pd.DataFrame(
                    data=player_list,
                    columns=valid_players.columns
                )
                # Add to a dictionary for later retrieving.
                name_dict[res] = choice

    print("Start calculating the maximum combination.")
    player_1()
    print("Finish calculating")
    print_result()

def print_result():
    check = 1
    # Convert to a maximum heap.
    heapq._heapify_max(score_heapq)
    while len(score_heapq) > 0:
        res = heapq._heappop_max(score_heapq)
        choice = name_dict[res]
        print(f"[{check} Choice]:")
        print(' ' * 10, 'Total Rating:', choice['RATING'].sum())
        print(' ' * 10, 'Total Scores:', round(res, 2))
        print('-' * 100)
        print(choice)
        print('-' * 100)
        check += 1
