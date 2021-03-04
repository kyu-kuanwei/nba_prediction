import datetime
import os


class DataPath:
    _DATA_PATH = "data"
    _SCRATH_PATH = "scratch"
    _STATIC_PATH = "static"
    _CSV_EXTENSION = ".csv"
    _NBA_PLAYERS = "nba_players"
    _NBA_TEAMS = "nba_teams"

    today_date = datetime.date.today()

    # Scratch files.
    _SCRATCH_DATA_FILE_NAME = str(today_date) + _CSV_EXTENSION

    SCRATCH_DATA_PATH = os.path.join(_DATA_PATH, _SCRATH_PATH)
    SCRATCH_DATA_FILE = os.path.join(SCRATCH_DATA_PATH, _SCRATCH_DATA_FILE_NAME)

    # Static files.
    _NBA_PLAYERS_DATA_FILE_NAME = _NBA_PLAYERS + _CSV_EXTENSION
    _NBA_TEAMS_DATA_FILE_NAME = _NBA_TEAMS + _CSV_EXTENSION

    STATIC_DATA_PATH = os.path.join(_DATA_PATH, _STATIC_PATH)
    NBA_PLAYERS_DATA_FILE = os.path.join(STATIC_DATA_PATH, _NBA_PLAYERS_DATA_FILE_NAME)
    NBA_TEAMS_DATA_FILE = os.path.join(STATIC_DATA_PATH, _NBA_TEAMS_DATA_FILE_NAME)