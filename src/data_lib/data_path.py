import datetime
import os

from src.utils.util import Date


class DataPath:
    # Parent directory.
    _DATA_PATH = "data"
    # Sub directories.
    _AVERAGE_PATH = "average"
    _AFTER_GAME = "after_game"
    _FANTASY_PATh = "fantasy"
    _SCRAPE_PATH = "scrape"
    _STATIC_PATH = "static"

    _NBA_PLAYERS = "nba_players"
    _NBA_TEAMS = "nba_teams"
    _NUMBER_FIVE = "number_five"
    _AVG = "average"

    _CSV_EXTENSION = ".csv"

    today_date = Date.today_date

    # Players averge stats files.
    PLAYER_AVG_PATH = os.path.join(_DATA_PATH, _AVERAGE_PATH, str(today_date))
    # Average mode.
    PLAYER_AVG_M_AVG_FILE = os.path.join(PLAYER_AVG_PATH, _AVG + _CSV_EXTENSION)

    # After game files.
    AFTER_GAME_PATH = os.path.join(_DATA_PATH, _AFTER_GAME)
    AFTER_GAME_FILE_PATH = os.path.join(_DATA_PATH, _AFTER_GAME, str(today_date))
    AFTER_GAME_FILE = os.path.join(AFTER_GAME_FILE_PATH, _AFTER_GAME + _CSV_EXTENSION)

    # Fantasy porjection files.
    NUMBER_FIVE_FILE = os.path.join(_DATA_PATH, _FANTASY_PATh, _NUMBER_FIVE + _CSV_EXTENSION)

    # Scrape files.
    _SCRAPE_DATA_FILE_NAME = str(today_date) + _CSV_EXTENSION

    SCRAPE_DATA_PATH = os.path.join(_DATA_PATH, _SCRAPE_PATH)
    SCRAPE_DATA_FILE = os.path.join(SCRAPE_DATA_PATH, _SCRAPE_DATA_FILE_NAME)

    # Static files.
    _NBA_PLAYERS_DATA_FILE_NAME = _NBA_PLAYERS + _CSV_EXTENSION
    _NBA_TEAMS_DATA_FILE_NAME = _NBA_TEAMS + _CSV_EXTENSION

    STATIC_DATA_PATH = os.path.join(_DATA_PATH, _STATIC_PATH)
    NBA_PLAYERS_DATA_FILE = os.path.join(STATIC_DATA_PATH, _NBA_PLAYERS_DATA_FILE_NAME)
    NBA_TEAMS_DATA_FILE = os.path.join(STATIC_DATA_PATH, _NBA_TEAMS_DATA_FILE_NAME)

