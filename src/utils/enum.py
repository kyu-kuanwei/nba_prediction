from enum import Enum, IntEnum


class SleepTime(IntEnum):
    SHORT_SLEEP_TIME = 2
    LONG_SLEEP_TIME = 5


class ErrorMessage(Enum):
    FACEBOOK_PAGE_OPEN_ERROR = "Could not open the Facebook login page."
    FACEBOOK_LOGIN_ERROR= "Could not login to the Facebook account."
    START_PLAYING_ERROR = "Could not access the playing page."
    SCRAPE_ERROR = "Could not scrape the player stats."

class Mode(Enum):
    NUMBER_FIVE = "Number_Five"
    AVERAGE = "Averge"