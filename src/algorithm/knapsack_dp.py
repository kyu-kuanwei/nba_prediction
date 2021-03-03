import pprint

from src.data_pipeline import DataPipeline


def recommand():
    data_pipeline = DataPipeline()
    MAXIMUM_RATING = 430

    players_list = data_pipeline.player_list
    players_num = len(players_list)

    dp = [[0 for _ in range(MAXIMUM_RATING + 1)] for _ in range(players_num + 1)]

    for i in range(players_num + 1):
        rating = players_list[i - 1].rating
        for r in range(MAXIMUM_RATING, rating, -1):
            dp[i][r] = max(dp[i - 1][r], dp[i - 1][r - rating] + players_list[i - 1].score)

    res = dp[players_num][MAXIMUM_RATING]
    player_name = []
    print("Total Scores:", res)

    cur_rating = MAXIMUM_RATING
    for i in range(players_num, 0, -1):
        if res <= 0:
            break
        if res == dp[i - 1][cur_rating]:
            continue
        else:
            player_name.append(players_list[i - 1])
            res = res - players_list[i - 1].score
            cur_rating = cur_rating - players_list[i - 1].rating
    pprint.pprint(player_name)