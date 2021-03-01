import ast
import datetime
import os
import time

import pandas as pd

from decouple import config
from selenium import webdriver

from .enum import ErrorMessage, SleepTime


class Scratch:

    _DATA_PATH = "data"
    _SCRATCH_FILE_NAME = "data"
    _TODAY_DATE = str(datetime.date.today())

    def __init__(self):
        self._SCRATCH_DATA_FILE = os.path.join(
            self._DATA_PATH, "_".join([self._SCRATCH_FILE_NAME, self._TODAY_DATE]) + ".csv"
        )
        self._load_env()
        # self._scratch()
        self._check_data()
        self._clean_dataframe()

    def _load_env(self):
        self._EXECUTABLE_PATH = config('EXECUTABLE_PATH')

        self._FACEBOOK_ACCOUNT = config('FACEBOOK_ACCOUNT')
        self._FACEBOOK_PASSWORD = config('FACEBOOK_PASSWORD')
        self._WEB_URL = config('URL')

    def _check_data(self):
        if os.path.exists(self._SCRATCH_DATA_FILE):
            self._nba_data = pd.read_csv(self._SCRATCH_DATA_FILE)
        else:
            self._scratch()

    def _scratch(self):
        self._browser = webdriver.Chrome(executable_path=self._EXECUTABLE_PATH)

        # Open UDN fantansy website.
        try:
            self._browser.get(self._WEB_URL)
            time.sleep(SleepTime.SHORT_SLEEP_TIME)
        except BaseException:
            print(f"Could not access {self._WEB_URL}")
            exit(101)

        # Open the Facebook login page.
        try:
            connect_fb_button = self._browser.find_element_by_class_name('btn-fb')
            connect_fb_button.click()
            time.sleep(SleepTime.SHORT_SLEEP_TIME)
        except BaseException:
            print(ErrorMessage.FACEBOOK_PAGE_OPEN_ERROR)
            exit(102)

        # Login to Facebook.
        try:
            account = self._browser.find_element_by_name('email')
            account.send_keys(self._FACEBOOK_ACCOUNT)
            password = self._browser.find_element_by_name('pass')
            password.send_keys(self._FACEBOOK_PASSWORD)
            login_button = self._browser.find_element_by_name('login')
            time.sleep(SleepTime.SHORT_SLEEP_TIME)
            login_button.click()
            time.sleep(SleepTime.LONG_SLEEP_TIME)
        except BaseException:
            print(ErrorMessage.FACEBOOK_LOGIN_ERROR)
            exit(103)

        # Start playing.
        try:
            start = self._browser.find_element_by_class_name('btn-play')
            start.click()
            time.sleep(SleepTime.SHORT_SLEEP_TIME)
        except BaseException:
            print(ErrorMessage.START_PLAYING_ERROR)
            exit(104)

        #Scrath results.
        try:
            # Tomorrow players.
            nba_state = self._browser.execute_script('return _NBA_STATE')
            # Current injured players.
            injured_players = self._browser.execute_script('return injuredPlayers')
            # Close browser.
            self._browser.close()
        except BaseException:
            print(ErrorMessage.SCRATCH_ERROR)
            exit(105)

        # Build dataframe.
        self._nba_data = pd.DataFrame(nba_state)
        # Filter out injured players.
        self._nba_data = self._nba_data[~self._nba_data.playerId.isin(injured_players)]

        self._export_to_csv()

    def _export_to_csv(self):
        # Export to a cache csv file.
        self._nba_data.to_csv(self._SCRATCH_DATA_FILE, index=False)

    def _clean_dataframe(self):
        # Merge players name.
        self._nba_data['PLAYER_NAME'] = self._nba_data.loc[:, ['firstName', 'lastName']].agg(' '.join, axis=1)
        # Filter and reorder columns.
        self._nba_data = self._nba_data.loc[:, ['PLAYER_NAME', 'position', 'team', 'rating']].reset_index(drop=True)
        # Convert rating to integer type.
        self._nba_data['rating'] = pd.to_numeric(self._nba_data['rating'], errors="coerce", downcast="integer")
        self._nba_data.dropna(inplace=True)

    @property
    def results(self) -> pd.DataFrame:
        return self._nba_data
