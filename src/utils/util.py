from datetime import date, timedelta


class Date:
    today_date = date.today()
    yesterday_date = date.today() - timedelta(days=1)

