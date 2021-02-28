import ast
import os
import time

import pandas as pd

from bs4 import BeautifulSoup
from decouple import config
from selenium import webdriver

from .common import Common


class Scratch:

    def __init__(self):
        self._load_env()
        self._browser = webdriver.Chrome(executable_path=self._EXECUTABLE_PATH)
        self._scratch()
        self._clean_dataframe()

    def _load_env(self):
        self._EXECUTABLE_PATH = config('EXECUTABLE_PATH')

        self._FACEBOOK_ACCOUNT = config('FACEBOOK_ACCOUNT')
        self._FACEBOOK_PASSWORD = config('FACEBOOK_PASSWORD')
        self._WEB_URL = config('URL')

    def _scratch(self):
        # Open UDN fantansy website.
        try:
            self._browser.get(self._WEB_URL)
            time.sleep(Common.SHORT_SLEEP_TIME)
        except BaseException:
            print(f"Could not access {self._WEB_URL}")
            exit(101)

        # Open the Facebook login page.
        try:
            connect_fb_button = self._browser.find_element_by_class_name('btn-fb')
            connect_fb_button.click()
            time.sleep(Common.SHORT_SLEEP_TIME)
        except BaseException:
            print("Could not open the Facebook login page.")
            exit(102)

        # Login to Facebook.
        try:
            account = self._browser.find_element_by_name('email')
            account.send_keys(self._FACEBOOK_ACCOUNT)
            password = self._browser.find_element_by_name('pass')
            password.send_keys(self._FACEBOOK_PASSWORD)
            login_button = self._browser.find_element_by_name('login')
            time.sleep(Common.SHORT_SLEEP_TIME)
            login_button.click()
            time.sleep(Common.LONG_SLEEP_TIME)
        except BaseException:
            print("Could not login to the Facebook account.")
            exit(103)

        # Start playing.
        try:
            start = self._browser.find_element_by_class_name('btn-play')
            start.click()
        except BaseException:
            print("Could not access the playing page.")
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
            print("Could not scratch the player stats.")
            exit(105)

        # Build dataframe.
        self._nba_data = pd.DataFrame(nba_state)
        # Filter out injured players.
        self._nba_data = self._nba_data[~self._nba_data.playerId.isin(injured_players)]

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
