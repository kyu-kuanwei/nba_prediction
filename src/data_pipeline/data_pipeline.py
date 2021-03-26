import os
from typing import List

import pandas as pd
from src.utils.enum import Mode

from .data_path import DataPath


class DataPipeline:

    def __init__(self, player_rating, player_stats):
        self._players_rating = player_rating
        self._players_stats = player_stats
        # Merge tomrrow players with all player stats.
        self._merge_data()
        # Clean data frame
        self._clean_data_frame()

    def _merge_data(self):
        self._valid_players = pd.merge(self._players_rating, self._players_stats, on='PLAYER_NAME')
        self._valid_players.columns = map(str.upper, self._valid_players.columns)

    def _clean_data_frame(self):
        position_map = {
            str(['F', 'G']): 'F-G',
            str(['G', 'F']): 'F-G',
            str(['F', 'C']): 'C-F',
            str(['C', 'F']): 'C-F',
            str(['G']): 'G',
            str(['F']): 'F',
            str(['C']): 'C',
        }
        self._valid_players = self._valid_players.replace({'POSITION': position_map})
        self._valid_players['AVG'] = self._valid_players['SCR'] / self._valid_players['RATING']
        self._valid_players.AVG = self._valid_players.AVG.round(2)
        self._valid_players.sort_values(by='AVG', inplace=True, ascending=False, ignore_index=True)
        self._valid_players = self._valid_players.loc[:70]

    def export_to_csv(self, mode=None):
        if mode:
            if not os.path.exists(DataPath.PLAYER_AVG_PATH):
                print(f"Create {DataPath.PLAYER_AVG_PATH} directory.")
                os.mkdir(DataPath.PLAYER_AVG_PATH)

            if mode == Mode.NUMBER_FIVE.value:
                print(
                    f"Export player performance based on mode [{mode}] "
                    f"to '{DataPath.PLAYER_AVG_M_NUM_FILE}'."
                )
                self._valid_players.to_csv(DataPath.PLAYER_AVG_M_NUM_FILE, index=False)
            elif mode == Mode.AVERAGE.value:
                print(
                    f"Export player performance based on mode [{mode}] "
                    f"to '{DataPath.PLAYER_AVG_M_AVG_FILE}'."
                )
                self._valid_players.to_csv(DataPath.PLAYER_AVG_M_AVG_FILE, index=False)
            elif mode == Mode.FAN_DUEL.value:
                print(
                    f"Export player performance based on mode [{mode}] "
                    f"to '{DataPath.PLAYER_AVG_M_FAN_FILE}'."
                )
                self._valid_players.to_csv(DataPath.PLAYER_AVG_M_FAN_FILE, index=False)
        else:
            print(f"Mode is [{mode}]. Don't export to csv file.")

    @property
    def valid_players(self) -> pd.DataFrame:
        return self._valid_players

