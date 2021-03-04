from fuzzywuzzy import fuzz
import pandas as pd
import requests
from bs4 import BeautifulSoup
from nba_api.stats.endpoints import leaguedashplayerstats
from nba_api.stats.static import teams

from .config import load_configs
from src.data_pipeline import DataPath

class PlayerStats:

    def __init__(self):
        self._load_configs()
        # Scratch from espn website to get the teams today.
        self._today_matchups: dict = {}
        self._all_players = self._find_players()
        self._injuries = self._injuries_players()
        # Filter out injuries.
        self._filter_injuries()

    def _load_configs(self):
        self._last_n_games = load_configs['last_n_games']
        self._injuries_url = load_configs['injuries_url']

    def _teams_play_today(self):
        today_date = DataPath.today_date.strftime('%T%m%d')
        espn_url = load_configs['espn_url'] + today_date

        r = requests.get(espn_url)
        content = r.content
        soup = BeautifulSoup(content, 'html.parser')
        for row in soup.select("table.schedule tbody tr"):
            home_team, away_team = row.select(".team-name")
            self._today_matchups[home_team.get_text().split(' ')[-1]] = away_team.get_text().split(' ')[-1]

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

    def _filter_injuries(self):
        for idx, player in enumerate(self._all_players['PLAYER_NAME']):
            for injury in self._injuries['Player']:
                # Check name.
                if fuzz.ratio(player, injury) >= 80:
                    self._all_players.drop(idx, inplace=True)
    @property
    def all_players(self):
        return self._all_players