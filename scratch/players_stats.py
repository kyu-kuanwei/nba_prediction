import pandas as pd
import requests
from bs4 import BeautifulSoup
from nba_api.stats.endpoints import leaguedashplayerstats
from nba_api.stats.static import teams

from .config import load_configs


class PlayerStats:

    def __init__(self):
        self._load_configs()
        self._all_players = self._find_players()
        self._injuries = self._injuries_players()
        # Filter out injuries.
        self._all_players = self._all_players[~self._all_players['PLAYER_NAME'].isin(self._injuries['Player'])]

    def _load_configs(self):
        self._last_n_games = load_configs['last_n_games']
        self._injuries_url = load_configs['injuries_url']

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

    def _injuries_players(self):
        # Get url content.
        url = requests.get(self._injuries_url)
        content = url.content
        # Parsed by beautifulsoup.
        soup = BeautifulSoup(content, 'html.parser')
        table = soup.find(name= 'div', attrs= {'class':'Page-colMain'})
        html_str = str(table)
        # Create dataframe.
        raw_injuries = pd.read_html(html_str)
        # Concate all dataframes.
        injuries = pd.concat(raw_injuries, ignore_index=True)
        # Clean injureis players.
        injuries['Player'] = injuries['Player'].apply(lambda x: x.split(' ', 2)[2])
        injuries = injuries.loc[:, ['Player']]

        return injuries

    @property
    def all_players(self):
        return self._all_players