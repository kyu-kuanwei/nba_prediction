import datetime
import os


class DataPath:
    _DATA_PATH = "data"
    _SCRATH_PATH = "scratch"
    _STATIC_PATH = "static"
    _CSV_EXTENSION = ".csv"
    _TODAY_DATE = str(datetime.date.today())
    _NBA_PLAYERS = "nba_players"
    _NBA_TEAMS = "nba_teams"

    # Scratch files.
    _SCRATH_DATA_FILE_NAME = _TODAY_DATE + _CSV_EXTENSION

    SCRATH_DATA_PATH = os.path.join(_DATA_PATH, _SCRATH_PATH)
    SCRATH_DATA_FILE = os.path.join(SCRATH_DATA_PATH, _SCRATH_DATA_FILE_NAME)

    # Static files.
    _NBA_PLAYERS_DATA_FILE_NAME = _NBA_PLAYERS + _CSV_EXTENSION
    _NBA_TEAMS_DATA_FILE_NAME = _NBA_TEAMS + _CSV_EXTENSION

    STATIC_DATA_PATH = os.path.join(_DATA_PATH, _STATIC_PATH)
    NBA_PLAYERS_DATA_FILE = os.path.join(STATIC_DATA_PATH, _NBA_PLAYERS_DATA_FILE_NAME)
    NBA_TEAMS_DATA_FILE = os.path.join(STATIC_DATA_PATH, _NBA_TEAMS_DATA_FILE_NAME)