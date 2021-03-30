import os
import pandas
from src.data_pipeline.data_path import DataPath


class TopTenPlayer:
    def __init__(self):
        self._top_ten_players = self._init_files()
        self._clean_top_ten_dataframe()

    def _init_files(self) -> pd.DataFrame:
        """Read csv files to the dataframe."""
        file_name = 'after_game.csv'
        dir_list = os.listdir(DataPath.AFTER_GAME_PATH)
        files = [os.path.join(DataPath.AFTER_GAME_PATH, d, file_name) for d in date_name]
        data = [pd.read_csv(f)[:10] for f in files]
        top_ten_players = pd.concat(data)

        return top_ten_players

    def _clean_top_ten_dataframe():
        self._top_ten_players = (
            self._top_ten_players.groupby(['PLAYER_NAME'])['TEAM'].count()
                .reset_index(name="COUNT")
                .sort_values(by='COUNT', ascending=False, ignore_index=True)
        )

    @property
    def top_ten_players(self) -> pd.DataFrame:
        return self._top_ten_players
