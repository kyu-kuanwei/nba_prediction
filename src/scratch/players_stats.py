import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup
from fuzzywuzzy import fuzz
from nba_api.stats.endpoints import leaguedashplayerstats
from nba_api.stats.static import teams
from src.data_pipeline import DataPath
from src.utils.enum import Mode

from .config import load_configs


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
        self._mode = load_configs['mode']
        self._last_n_games = load_configs['last_n_games']
        self._injuries_url = load_configs['injuries_url']
        self._number_five_url = load_configs['number_five_url']

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
        if self._mode == Mode.FAN_DUEL.value:
            print(f"The mode is {self._mode}. Use the dataset from '{DataPath.FAN_DUEL_FILE}'.")
            all_players = self._mode_fantasy_projections(DataPath.FAN_DUEL_FILE)
        elif self._mode == Mode.DRAFT_KINGS.value:
            print(f"The mode is {self._mode}. Use the dataset from '{DataPath.DRAFT_KINGS_FILE}'.")
            all_players = self._mode_fantasy_projections(DataPath.DRAFT_KINGS_FILE)
        elif self._mode == Mode.NUMBER_FIVE.value:
            print(f"The mode is {self._mode}. Use the dataset from '{DataPath.NUMBER_FIVE_FILE}'.")
            stats = self._scratch_numberfive()
            df = self._mode_number_five_clean_dataframe(stats)
            all_players = self._mode_number_five_projections(DataPath.NUMBER_FIVE_FILE)
        else:
            # Default
            print(f"The mode is {self._mode}. Use the dataset from 'nba_api'.")
            all_players = self._mode_average_stats()

        return all_players

    def _scratch_numberfive(self) -> list:
        print("Start scracthing data from number five website.")
        url = self._number_five_url
        page = requests.get(url)
        content = page.content
        soup = BeautifulSoup(content, 'html.parser')
        stats = []
        for tr in soup.find_all('tr'):
            tds = tr.find_all('td')
            try:
                name = tr.find_all('a')
                clean = [t.text.strip() for t in tds]
                clean.append(name[1].text.strip())
                stats.append(clean[5:])
            except:
                continue
        print("Finish scratching number five data.")

        return stats

    def _mode_number_five_clean_dataframe(self, stats: list):
        col_names = ['PTS', 'REB', 'AST', 'STL', 'BLK', 'TOV', 'Name']
        df = pd.DataFrame(np.array(stats), columns=col_names)
        df = df[['Name', 'PTS', 'REB', 'AST', 'STL', 'BLK', 'TOV']]
        df['PTS'] = pd.to_numeric(df['PTS'], errors="coerce", downcast="float")
        df['REB'] = pd.to_numeric(df['REB'], errors="coerce", downcast="float")
        df['AST'] = pd.to_numeric(df['AST'], errors="coerce", downcast="float")
        df['STL'] = pd.to_numeric(df['STL'], errors="coerce", downcast="float")
        df['BLK'] = pd.to_numeric(df['BLK'], errors="coerce", downcast="float")
        df['TOV'] = pd.to_numeric(df['TOV'], errors="coerce", downcast="float")
        df.dropna(inplace=True)
        df['Name'] = df['Name'].convert_dtypes()
        df = df.round(2)

        print(f"Export the scracthed data to {DataPath.NUMBER_FIVE_FILE}")
        df.to_csv(DataPath.NUMBER_FIVE_FILE)

    def _mode_number_five_projections(self, data_path):
        all_players = pd.read_csv(data_path)
        all_players = all_players.loc[:, ['Name', 'PTS', 'REB', 'AST', 'STL', 'BLK', 'TOV']]
        all_players = all_players.rename(columns={'Name' : 'PLAYER_NAME'})
        all_players['SCR'] = (
            all_players['PTS']
            + all_players['REB'] * 1.2
            + all_players['AST'] * 1.5
            + all_players['STL'] * 3
            + all_players['BLK'] * 3
            - all_players['TOV']
        )
        return all_players.round(2)

    def _mode_fantasy_projections(self, data_path) -> pd.DataFrame:
        all_players = pd.read_csv(data_path)
        all_players = all_players.loc[:, ['Name', 'PTS', 'REB', 'AST', 'STL', 'BLK']]
        all_players = all_players.rename(columns={'Name' : 'PLAYER_NAME'})
        all_players['SCR'] = (
            all_players['PTS']
            + all_players['REB'] * 1.2
            + all_players['AST'] * 1.5
            + all_players['STL'] * 3
            + all_players['BLK'] * 3
        )
        return all_players.round(2)

    def _mode_average_stats(self) -> pd.DataFrame:
        all_players = leaguedashplayerstats.LeagueDashPlayerStats(last_n_games=self._last_n_games)
        all_players = all_players.get_data_frames()[0]
        all_players.loc[:, ['PTS', 'REB', 'AST', 'TOV', 'STL', 'BLK']] = (
            all_players.loc[:, ['PTS', 'REB', 'AST', 'TOV', 'STL', 'BLK']].div(all_players.GP, axis=0)
        )
        all_players = all_players.loc[:, ['PLAYER_NAME', 'GP', 'PTS', 'REB', 'AST', 'TOV', 'STL', 'BLK']]
        all_players = all_players[all_players.GP > 1].reset_index(drop=True)
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