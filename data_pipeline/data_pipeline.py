import pandas as pd
from scratch import AllPlayerStats, Scratch


class DataPipeline:

    def __init__(self):
        self._scratch = Scratch()
        self._all_players_stats = AllPlayerStats()

        self._tomorrow_players = self._scratch.results
        self._all_players = self._all_players_stats.all_players

        self._merge_data()

    def _merge_data(self):
        self._valid_players = pd.merge(self._tomorrow_players, self._all_players, on='PLAYER_NAME')
        self._valid_players.columns = map(str.upper, self._valid_players.columns)

    @property
    def valid_players(self) -> pd.DataFrame:
        return self._valid_players
