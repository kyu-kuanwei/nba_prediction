import pandas as pd

from yaml import safe_load
from nba_api.stats.static import teams
from nba_api.stats.endpoints import leaguedashplayerstats


class AllPlayerStats:

    def __init__(self):
        self._load_configs()
        self._all_players = self._find_players()

    def _load_configs(self):
        with open('config.yml') as f:
            self._config = safe_load(f)

        self._last_n_games = self._config['last_n_games']

    def _find_players(self):
        # Find all players.
        all_players = leaguedashplayerstats.LeagueDashPlayerStats(last_n_games=self._last_n_games)
        all_players = all_players.get_data_frames()[0]

        all_players.loc[:, ['PTS', 'REB', 'AST', 'TOV', 'STL', 'BLK']] = (
            all_players.loc[:, ['PTS', 'REB', 'AST', 'TOV', 'STL', 'BLK']].div(all_players.GP, axis=0)
        )
        all_players = all_players.loc[:, ['PLAYER_NAME', 'PTS', 'REB', 'AST', 'TOV', 'STL', 'BLK']]
        all_players['SCR'] = (
            all_players['PTS']
            + all_players['REB'] * 1.2
            + all_players['AST'] * 1.5
            + all_players['STL'] * 3
            + all_players['BLK'] * 3
            - all_players['TOV']
        )

        return all_players.round(2)

    @property
    def all_players(self):
        return self._all_players