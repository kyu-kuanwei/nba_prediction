import pandas as pd
from scratch import PlayerStats, Scratch

from .players import Players

from typing import List

class DataPipeline:

    def __init__(self):
        scratch = Scratch()
        all_players_stats = PlayerStats()

        self._tomorrow_players = scratch.results
        self._players_stats = all_players_stats.all_players
        # Merge tomrrow players with all player stats.
        self._merge_data()
        # Create a list of player object.
        self._build_players_list()


    def _merge_data(self):
        self._valid_players = pd.merge(self._tomorrow_players, self._players_stats, on='PLAYER_NAME')
        self._valid_players.columns = map(str.upper, self._valid_players.columns)

    def _build_players_list(self):
        self._player_list = [
            Players(
                name=row['PLAYER_NAME'],
                rating=row['RATING'],
                score=int(round(row['SCR'])),
                position=row['POSITION']
            ) for _, row in self._valid_players.iterrows()
        ]

    @property
    def valid_players(self) -> pd.DataFrame:
        return self._valid_players

    @property
    def player_list(self) -> List[Players]:
        return self._player_list
