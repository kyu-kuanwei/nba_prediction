from datetime import date, timedelta

from yaml import safe_load


class Date:
    today_date = date.today()
    yesterday_date = date.today() - timedelta(days=1)


class LoadConfig:
    with open('config.yml') as f:
        config = safe_load(f)
