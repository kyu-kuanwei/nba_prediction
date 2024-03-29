import ast
import datetime
import os
import time

import pandas as pd
from decouple import config
from selenium import webdriver
from src.data_lib import DataPath
from src.utils.enum import ErrorMessage, SleepTime
from src.utils.util import LoadConfig


class UdnScraper:

    def __init__(self):
        # Load enviornment variables.
        self._load_env()
        self._check_data()

    def _load_env(self):
        self._EXECUTABLE_PATH = config('EXECUTABLE_PATH')
        self._FACEBOOK_ACCOUNT = config('FACEBOOK_ACCOUNT')
        self._FACEBOOK_PASSWORD = config('FACEBOOK_PASSWORD')

        self._WEB_URL = LoadConfig.config['fantasy_url']

    def _check_data(self):
        # If the file exists, use the csv file.
        if os.path.exists(DataPath.SCRAPE_DATA_FILE):
            print(f"File '{DataPath.SCRAPE_DATA_FILE}' exists. Skip web scraping.")
            self._nba_data = pd.read_csv(DataPath.SCRAPE_DATA_FILE)
        else:
            # If the directory doesn't exist, create one.
            if not os.path.exists(DataPath.SCRAPE_DATA_PATH):
                print(f"File '{DataPath.SCRAPE_DATA_PATH}' doesn't exist. Create a directory.")
                # Make data directory.
                os.mkdir(DataPath.SCRAPE_DATA_PATH)

            # Scraping from the website.
            print("Start web scraping player info from UDN website.")
            self._scrape_udn()
            print("Finish scraping.")

            # Clean dataframe
            self._clean_udn_dataframe()
            # Export to a csv file.
            self._export_to_csv(file_name=DataPath.SCRAPE_DATA_FILE, data_frame=self._nba_data)

    def _scrape_udn(self):
        option = webdriver.ChromeOptions()
        option.add_argument("headless")
        self._browser = webdriver.Chrome(chrome_options=option, executable_path=self._EXECUTABLE_PATH)
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
            print(ErrorMessage.FACEBOOK_PAGE_OPEN_ERROR.value)
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
            print(ErrorMessage.FACEBOOK_LOGIN_ERROR.value)
            exit(103)

        # Start playing.
        try:
            start = self._browser.find_element_by_class_name('btn-play')
            start.click()
            time.sleep(SleepTime.SHORT_SLEEP_TIME)
        except BaseException:
            print(ErrorMessage.START_PLAYING_ERROR.value)
            exit(104)

        #Scrape results.
        try:
            # Tomorrow players.
            nba_state = self._browser.execute_script('return _NBA_STATE')
            # Current injured players.
            injured_players = self._browser.execute_script('return injuredPlayers')
            # Close browser.
            self._browser.close()
        except BaseException:
            print(ErrorMessage.SCRAPE_ERROR.value)
            exit(105)

        # Build dataframe.
        self._nba_data = pd.DataFrame(nba_state)
        # Filter out injured players.
        self._nba_data = self._nba_data[~self._nba_data.playerId.isin(injured_players)]

    def _clean_udn_dataframe(self):
        # Merge players name.
        self._nba_data['PLAYER_NAME'] = self._nba_data.loc[:, ['firstName', 'lastName']].agg(' '.join, axis=1)
        # Filter and reorder columns.
        self._nba_data = self._nba_data.loc[:, ['PLAYER_NAME', 'position', 'team', 'rating']].reset_index(drop=True)
        # Convert rating to integer type.
        self._nba_data['rating'] = pd.to_numeric(self._nba_data['rating'], errors="coerce", downcast="integer")
        self._nba_data.dropna(inplace=True)
        self._nba_data['position'] = self._nba_data['position'].apply(lambda x: str(x))

    def _export_to_csv(self, file_name: str, data_frame: pd.DataFrame):
        # Export to a cache csv file.
        data_frame.to_csv(file_name, index=False)

    @property
    def results(self) -> pd.DataFrame:
        return self._nba_data
