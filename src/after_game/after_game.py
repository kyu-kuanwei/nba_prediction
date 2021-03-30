import os
import pandas as pd

from src.utils.util import Date
from src.data_pipeline import DataPath, DataPipeline

from nba_api.stats.endpoints import leaguegamefinder
from nba_api.stats.endpoints import boxscoretraditionalv2


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
            players_rating=self._players_rating,
            all_players_today=self._all_players_today
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

    def _clean_data_frame(self, players_rating, all_players_today):
        data_pipeline = DataPipeline(
            player_rating=players_rating,
            player_stats=all_players_today
        )

        return data_pipeline.valid_players

    def _export_to_csv(self):
        if not os.path.exists(DataPath.AFTER_GAME_PATH):
            print(f"{DataPath.AFTER_GAME_PATH} doest not exist. Create the directory.")
            os.mkdir(DataPath.AFTER_GAME_PATH)

        if not os.path.exists(DataPath.AFTER_GAME_FILE):
            print(f"Export {DataPath.AFTER_GAME_FILE} file.")
            self._valid_players.to_csv(DataPath.AFTER_GAME_FILE, index=False)

    @property
    def top_ten_players(self):
        return self._all_players_today[:10]

    @property
    def valid_players(self):
        return self._valid_players