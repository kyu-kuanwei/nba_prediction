from enum import Enum, IntEnum


class SleepTime(IntEnum):
    SHORT_SLEEP_TIME = 2
    LONG_SLEEP_TIME = 5


class ErrorMessage(Enum):
    FACEBOOK_PAGE_OPEN_ERROR = "Could not open the Facebook login page."
    FACEBOOK_LOGIN_ERROR= "Could not login to the Facebook account."
    START_PLAYING_ERROR = "Could not access the playing page."
    SCRATCH_ERROR = "Could not scratch the player stats."

class Mode(Enum):
    FAN_DUEL = "Fan_Duel"
    DRAFT_KINGS = "Draft_Kings"
    NUMBER_FIVE = "Number_Five"
    AVERAGE = "Averge"