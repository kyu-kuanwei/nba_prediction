import datetime
import os


class DataPath:
    # Parent directory.
    _DATA_PATH = "data"
    # Sub directories.
    _SCRAPE_PATH = "scrape"
    _STATIC_PATH = "static"
    _FANTASY = "fantasy"

    _NBA_PLAYERS = "nba_players"
    _NBA_TEAMS = "nba_teams"
    _FAN_DUEL = "fan_duel"
    _DRAFT_KINGS = "draft_kings"
    _NUMBER_FIVE = "number_five"

    _CSV_EXTENSION = ".csv"

    today_date = datetime.date.today()

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

    # Fantasy porjection files.
    FAN_DUEL_FILE = os.path.join(_DATA_PATH, _FANTASY, _FAN_DUEL + _CSV_EXTENSION)
    DRAFT_KINGS_FILE = os.path.join(_DATA_PATH, _FANTASY, _DRAFT_KINGS + _CSV_EXTENSION)
    NUMBER_FIVE_FILE = os.path.join(_DATA_PATH, _FANTASY, _NUMBER_FIVE + _CSV_EXTENSION)
