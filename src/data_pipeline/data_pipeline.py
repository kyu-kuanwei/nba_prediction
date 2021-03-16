import os
from typing import List

import pandas as pd
from src.scrape import load_configs, PlayerStats, Scraper
from src.utils.enum import Mode

from .data_path import DataPath
from .players import Players


class DataPipeline:

    def __init__(self):
        scraper = Scraper()
        all_players_stats = PlayerStats()

        self._tomorrow_players = scraper.results
        self._players_stats = all_players_stats.all_players
        # Merge tomrrow players with all player stats.
        self._merge_data()
        # Clean data frame
        self._clean_data_frame()
        # Create a list of player object.
        self._build_players_list()
        # Export today results as an csv file.
        self._export_to_csv()

    def _merge_data(self):
        self._valid_players = pd.merge(self._tomorrow_players, self._players_stats, on='PLAYER_NAME')
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
        self._valid_players = self._valid_players.loc[:80]

    def _build_players_list(self):
        self._player_list = [
            Players(
                name=row['PLAYER_NAME'],
                rating=row['RATING'],
                score=int(round(row['SCR'])),
                position=row['POSITION']
            ) for _, row in self._valid_players.iterrows()
        ]

    def _export_to_csv(self):
        if not os.path.exists(DataPath.PLAYER_AVG_PATH):
            print(f"Create {DataPath.PLAYER_AVG_PATH} directory.")
            os.mkdir(DataPath.PLAYER_AVG_PATH)

        mode = load_configs['mode']

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
            print("Mode is unknown.")

    @property
    def valid_players(self) -> pd.DataFrame:
        return self._valid_players

    @property
    def player_list(self) -> List[Players]:
        return self._player_list
