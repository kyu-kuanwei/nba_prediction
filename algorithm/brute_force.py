from data_pipeline import DataPipeline
import numpy as np
import pandas as pd

def recommand():
    data_pipeline = DataPipeline()

    players_list = data_pipeline.valid_players

    position_trans = {
        str(['F', 'G']): 'F-G',
        str(['G', 'F']): 'F-G',
        str(['F', 'C']): 'C-F',
        str(['C', 'F']): 'C-F',
        str(['G']): 'G',
        str(['F']): 'F',
        str(['C']): 'C',
        str(['F', 'F']): 'F',
        str(['G', 'G']): 'G',
        str(['C', 'C']): 'C'
    }
    players_list = players_list.replace({'POSITION': position_trans})
    players_list['AVG'] = players_list['SCR'] / players_list['RATING']
    players_list.sort_values(by='AVG', inplace=True, ascending=False, ignore_index=True)
    players_list = players_list[:70]
    # players_list = players_list[players_list.RATING >= 70]

    guards = players_list[(players_list.POSITION == "G") | (players_list.POSITION == "F-G")]
    forwards = players_list[
        (players_list.POSITION == "F")
        | (players_list.POSITION == "F-G")
        | (players_list.POSITION == "C-F")
    ]
    centers = players_list[(players_list.POSITION == "C") | (players_list.POSITION == "C-F")]

    # guard_list = guards.loc[:, ['PLAYER_NAME', 'RATING', 'SCR']].to_numpy()
    # forward_list = forwards.loc[:, ['PLAYER_NAME', 'RATING', 'SCR']].to_numpy()
    # center_list = centers.loc[:, ['PLAYER_NAME', 'RATING', 'SCR']].to_numpy()

    guard_list = guards.to_numpy()
    forward_list = forwards.to_numpy()
    center_list = centers.to_numpy()

    global res
    res = 0
    name_list = []

    def player_1():
        for idx1 in range(len(guard_list)):
            # player1 = guard_list[idx1]
            player_2(idx1)

    def player_2(idx1):
        for idx2 in range(idx1+1, len(guard_list)):
            # player2 = guard_list[idx2]
            if len({guard_list[idx1][0], guard_list[idx2][0]}) == 2:
                player_3(idx1, idx2)

    def player_3(idx1, idx2):
        for idx3 in range(len(forward_list)):
            # player3 = forward_list[idx3]
            if len({guard_list[idx1][0], guard_list[idx2][0], forward_list[idx3][0]}) == 3:
                player_4(idx1, idx2, idx3)

    def player_4(idx1, idx2, idx3):
        for idx4 in range(idx3+1, len(forward_list)):
            # player4 = forward_list[idx4]
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
                    columns=players_list.columns
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

