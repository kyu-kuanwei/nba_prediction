import os

import pandas as pd
from nba_api.stats.endpoints import boxscoretraditionalv2, leaguegamefinder
from src.data_lib import DataPath
from src.utils.util import Date


class AfterGame:
    def __init__(self):
        # Generate nba api date format. Due to the time difference, use yesterday date.
        self._date_nba_api_format = Date.yesterday_date.strftime("%m/%d/%Y")
        # Generate yesterdat date format to get csv file.
        self._date_csv_format = Date.yesterday_date.strftime("%Y-%m-%d") + ".csv"

        # Get matchups today.
        self._today_games = self._today_matchups()
        # Get all stats today.
        self._all_players_today = self._players_stats()
        # Get players' rating. (Scrape from yesterday)
        self._players_rating = self._find_player_rating()
        # Merge and clean players dataframe.
        self._valid_players = self._clean_data_frame(
            df1=self._players_rating,
            df2=self._all_players_today
        )
        # Export to the csv file.
        self._export_to_csv()

    def _today_matchups(self) -> pd.DataFrame:
        gamefinder = leaguegamefinder.LeagueGameFinder(
            league_id_nullable='00',
            date_from_nullable=self._date_nba_api_format
        )
        today_games = gamefinder.get_data_frames()[0]

        return today_games

    def _players_stats(self) -> pd.DataFrame:
        col = ['PLAYER_NAME', 'PTS', 'REB', 'AST', 'STL', 'BLK', 'TO']

        # Get player stats today.
        game_ids = self._today_games['GAME_ID'].unique()
        players_today = []
        for game_id in game_ids:
            b = boxscoretraditionalv2.BoxScoreTraditionalV2(game_id=game_id).get_data_frames()[0]
            players_today.append(b)

        # Concat to a dataframe.
        all_players_today = pd.concat(players_today)
        all_players_today = all_players_today.loc[:, col]
        all_players_today = all_players_today.fillna(0)
        all_players_today = all_players_today.reset_index(drop=True)

        all_players_today.rename(columns={'TO':'TOV'}, inplace=True)
        all_players_today['SCR'] = (
            all_players_today['PTS']
            + all_players_today['REB'] * 1.2
            + all_players_today['AST'] * 1.5
            + all_players_today['STL'] * 3
            + all_players_today['BLK'] * 3
            - all_players_today['TOV']
        )
        all_players_today.sort_values(by='SCR', ignore_index=True, inplace=True, ascending=False)

        return all_players_today

    def _find_player_rating(self):
        scrape_data_file = os.path.join(DataPath.SCRAPE_DATA_PATH, self._date_csv_format)
        players_rating = pd.read_csv(scrape_data_file)

        return players_rating

    def _clean_data_frame(self, df1, df2):
        valid_players = pd.merge(df1, df2, on='PLAYER_NAME')
        valid_players.columns = map(str.upper, valid_players.columns)

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
        valid_players['AVG'] = valid_players['SCR'] / valid_players['RATING']
        valid_players.AVG = valid_players.AVG.round(2)
        valid_players.sort_values(by='AVG', inplace=True, ascending=False, ignore_index=True)

        return valid_players.loc[:70]

    def _export_to_csv(self):
        if not os.path.exists(DataPath.AFTER_GAME_FILE_PATH):
            print(f"{DataPath.AFTER_GAME_FILE_PATH} doest not exist. Create the directory.")
            os.mkdir(DataPath.AFTER_GAME_FILE_PATH)

        if not os.path.exists(DataPath.AFTER_GAME_FILE):
            print(f"Export {DataPath.AFTER_GAME_FILE} file.")
            self._valid_players.to_csv(DataPath.AFTER_GAME_FILE, index=False)

    @property
    def top_ten_players(self):
        return self._all_players_today[:10]

    @property
    def valid_players(self):
        return self._valid_players