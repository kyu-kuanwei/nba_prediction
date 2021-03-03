from src.data_pipeline import DataPipeline
import numpy as np
import pandas as pd

def recommand():
    data_pipeline = DataPipeline()

    valid_players = data_pipeline.valid_players

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

    global res
    res = 0
    name_list = []

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
        global res
        for idx5 in range(len(center_list)):
            player1 = guard_list[idx1]
            player2 = guard_list[idx2]
            player3 = forward_list[idx3]
            player4 = forward_list[idx4]
            player5 = center_list[idx5]
            if (len({player1[0], player2[0], player3[0], player4[0], player5[0]}) == 5
            ) and (
                player1[3] + player2[3] + player3[3] + player4[3] + player5[3] <= 430
            ) and (
                player1[-2] + player2[-2] + player3[-2] + player4[-2] + player5[-2] > res
            ):
                res = player1[-2] + player2[-2] + player3[-2] + player4[-2] + player5[-2]
                choice = pd.DataFrame(
                    data=[player1, player2, player3, player4, player5],
                    columns=valid_players.columns
                )
                name_list.append(choice)

    player_1()

    K = 1
    while K <= 2:
        print(f"[{K} Choice]:")
        print(' ' * 10, 'Total Rating:', name_list[-K]['RATING'].sum())
        print(' ' * 10, 'Total Scores:', round(name_list[-K]['SCR'].sum(), 2))
        print('-' * 100)
        print(name_list[-K])
        print('-' * 100)
        K += 1

