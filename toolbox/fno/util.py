import calendar
import re
from datetime import date, timedelta

from dateutil.relativedelta import relativedelta

from toolbox.datetime.util import get_datetime_now


def get_futures_tradingsymbol(tradingsymbol, cycle, time_zone):
    """
    Try cast options and futures trading symbol to underlying futures trading symbol.
    https://kite.trade/forum/discussion/6778/nifty-bank-nifty-trading-symbol-for-jan-2020-weekly-contracts
    https://kite.trade/forum/discussion/5574/change-in-format-of-weekly-options-instruments
    :param tradingsymbol:
    :param cycle:
    :param time_zone:
    :return:
    """
    KNOWN_SYMBOLS = {
        'NIFTY 50': 'NIFTY',
        'NIFTY BANK': 'BANKNIFTY'
    }

    tradingsymbol = KNOWN_SYMBOLS.get(tradingsymbol, tradingsymbol)

    if tradingsymbol[-3:] == 'FUT':
        return tradingsymbol
    else:
        spot_name = re.sub('\d{2}[A-Z]{3}\d+[A-Z]{2}', '', tradingsymbol)  # trimming with monthly regex
        if spot_name.__len__() == tradingsymbol.__len__():
            spot_name = re.sub('\d{2}[1-9OND]\d{2}\d+[CP]E', '', tradingsymbol)  # trimming with weekly regex

    dt_cur = get_datetime_now(time_zone)

    if cycle == 'current':
        dt_thursday = get_last_day_of_month(dt_cur.date().year, dt_cur.date().month, day='Thursday')
        if dt_thursday < dt_cur.date():
            dt_cur = get_datetime_now(time_zone) + relativedelta(months=1)
    elif cycle == 'mid':
        dt_cur = dt_cur + relativedelta(months=1)
        dt_thursday = get_last_day_of_month(dt_cur.date().year, dt_cur.date().month, day='Thursday')
        if dt_thursday < dt_cur.date():
            dt_cur = get_datetime_now(time_zone) + relativedelta(months=1)
    elif cycle == 'far':
        dt_cur = dt_cur + relativedelta(months=2)
        dt_thursday = get_last_day_of_month(dt_cur.date().year, dt_cur.date().month, day='Thursday')
        if dt_thursday < dt_cur.date():
            dt_cur = get_datetime_now(time_zone) + relativedelta(months=1)
    else:
        raise NotImplementedError()

    return f'{spot_name}{dt_cur.strftime("%y%b")}FUT'.upper()


def get_last_day_of_month(year, month, day='Thursday'):
    daysInMonth = calendar.monthrange(year, month)[1]  # Returns (month, numberOfDaysInMonth)
    dt = date(year, month, daysInMonth)

    d = {'Monday': 1, 'Tuesday': 2, 'Wednesday': 3, 'Thursday': 4, 'Friday': 5, 'Saturday': 6, 'Sunday': 7}
    offset = d[day] - dt.isoweekday()
    if offset > 0:
        offset -= 7  # Back up one week if necessary

    dt += timedelta(offset)
    return dt  # date
