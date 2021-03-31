import os
from typing import List

import pandas as pd
from src.data_lib import DataPath, TopTenPlayers
from src.scrape import PlayerStats, Scraper, load_configs
from src.utils.enum import Mode


class DataPipeline:

    def __init__(self):
        mode = load_configs["mode"]

        scraper = Scraper()
        all_players_stats = PlayerStats()

        # Merge tomrrow players with all player stats.
        valid_players = self._merge_data(df1=scraper.results, df2=all_players_stats.all_players)
        # Merge historical top ten players.
        valid_players = self._merge_top_ten_players(
            top_ten_players=TopTenPlayers().history_top_ten_players,
            valid_players=valid_players
        )
        # Clean data frame
        self._valid_players = self.clean_data_frame(valid_players=valid_players, mode=mode)
        # Export to csv file.
        self.export_to_csv(valid_players=self._valid_players, mode=mode)

    def _merge_data(self, df1, df2) -> pd.DataFrame:
        valid_players = pd.merge(df1, df2, on='PLAYER_NAME')
        valid_players.columns = map(str.upper, valid_players.columns)


        return valid_players

    def _merge_top_ten_players(self, top_ten_players, valid_players):
        mapping = dict(top_ten_players[['PLAYER_NAME', 'COUNT']].values)
        valid_players['TOP_TEN'] = valid_players.PLAYER_NAME.map(mapping)
        valid_players['TOP_TEN'] = valid_players['TOP_TEN'].fillna(0)

        return valid_players

    def clean_data_frame(self, valid_players, mode):
        position_map = {
            str(['F', 'G']): 'F-G',
            str(['G', 'F']): 'F-G',
            str(['F', 'C']): 'C-F',
            str(['C', 'F']): 'C-F',
            str(['G']): 'G',
            str(['F']): 'F',
            str(['C']): 'C',
        }
        valid_players = valid_players.replace({'POSITION': position_map})
        # AVG calculated by the original SCR (not includes top ten times).
        valid_players['AVG'] = valid_players['SCR'] / valid_players['RATING']
        valid_players.AVG = valid_players.AVG.round(2)
        # The top ten times will be weighted to effect the final 'SCR'.
        valid_players['SCR'] = valid_players['SCR'] + valid_players['TOP_TEN'] * 2
        valid_players.sort_values(by='AVG', inplace=True, ascending=False, ignore_index=True)

        column_names = []
        if mode == Mode.NUMBER_FIVE.value:
            column_names = [
                "PLAYER_NAME", "POSITION", "TEAM", "RATING", "TOP_TEN",
                "PTS", "REB", "AST", "STL", "BLK", "TOV", "SCR", "AVG"
            ]
        else:
            column_names = [
                "PLAYER_NAME", "POSITION", "TEAM", "RATING", "GP", "TOP_TEN",
                "PTS", "REB", "AST", "STL", "BLK", "TOV", "SCR", "AVG"
            ]

        valid_players = valid_players.reindex(columns=column_names)

        return valid_players.loc[:70]

    def export_to_csv(self, valid_players, mode=None):
        if mode:
            if not os.path.exists(DataPath.PLAYER_AVG_PATH):
                print(f"Create {DataPath.PLAYER_AVG_PATH} directory.")
                os.mkdir(DataPath.PLAYER_AVG_PATH)

            if mode == Mode.NUMBER_FIVE.value:
                print(
                    f"Export player performance based on mode [{mode}] "
                    f"to '{DataPath.PLAYER_AVG_M_NUM_FILE}'."
                )
                valid_players.to_csv(DataPath.PLAYER_AVG_M_NUM_FILE, index=False)
            elif mode == Mode.AVERAGE.value:
                print(
                    f"Export player performance based on mode [{mode}] "
                    f"to '{DataPath.PLAYER_AVG_M_AVG_FILE}'."
                )
                valid_players.to_csv(DataPath.PLAYER_AVG_M_AVG_FILE, index=False)
            elif mode == Mode.FAN_DUEL.value:
                print(
                    f"Export player performance based on mode [{mode}] "
                    f"to '{DataPath.PLAYER_AVG_M_FAN_FILE}'."
                )
                valid_players.to_csv(DataPath.PLAYER_AVG_M_FAN_FILE, index=False)
        else:
            print(f"Mode is [{mode}]. Don't export to csv file.")

    @property
    def valid_players(self) -> pd.DataFrame:
        return self._valid_players
