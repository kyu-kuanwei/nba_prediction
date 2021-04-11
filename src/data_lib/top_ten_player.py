import os

import pandas as pd
from src.data_lib.data_path import DataPath


class TopTenPlayers:
    def __init__(self):
        top_ten_players = self._init_files()
        self._top_ten_players = self._clean_top_ten_dataframe(top_ten_players=top_ten_players)

    def _init_files(self) -> pd.DataFrame:
        """Read csv files to the dataframe."""
        file_name = 'after_game.csv'
        dir_list = os.listdir(DataPath.AFTER_GAME_PATH)
        files = [os.path.join(DataPath.AFTER_GAME_PATH, d, file_name) for d in dir_list]
        data = [pd.read_csv(f)[:5] for f in files]
        top_ten_players = pd.concat(data)

        return top_ten_players

    def _clean_top_ten_dataframe(self, top_ten_players):
        clean_top_ten_players = (
            top_ten_players.groupby(['PLAYER_NAME'])['TEAM'].count()
                .reset_index(name="COUNT")
                .sort_values(by='COUNT', ascending=False, ignore_index=True)
        )

        return clean_top_ten_players

    @property
    def history_top_ten_players(self) -> pd.DataFrame:
        return self._top_ten_players
