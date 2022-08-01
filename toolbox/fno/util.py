import calendar
import re
from datetime import date, timedelta

from dateutil.relativedelta import relativedelta

from toolbox.datetime.util import get_date_now
from toolbox.datetime.util import get_datetime_now
from toolbox.math.util import round_nearest


def get_options_ts_current_exp(session, model, time_zone):
    record = session.query(model).filter(model.expiry_date >= get_date_now(time_zone), ).first()
    return {'expiry_date': record.expiry_date, 'expiry_type': record.expiry_type}


def get_options_ts_current_5(tradingsymbol, session, exp_model, time_zone, und_ref_price, strike_space, strike_size):
    result = get_options_ts_current_exp(session, exp_model, time_zone)
    exp_date = result['expiry_date']
    exp_type = result['expiry_type']

    # Generate references
    und_ref_price = float(und_ref_price)  # underlying reference price
    und_ref_strike = round_nearest(und_ref_price, strike_size)
    min_strike = und_ref_strike - strike_size * strike_space
    max_strike = und_ref_strike + strike_size * strike_space

    results_CE, results_PE = [], []
    for strike in range(min_strike, max_strike + 1, strike_size):
        results_CE.append(get_options_tradingsymbol(tradingsymbol, strike, exp_date, 'CE', exp_type))
        results_PE.append(get_options_tradingsymbol(tradingsymbol, strike, exp_date, 'PE', exp_type))
    return results_CE, results_PE


def get_options_tradingsymbol(tradingsymbol, strike, dt_exp, opt_type, exp_type):
    """
    Try cast options and futures trading symbol to underlying futures trading symbol.
    https://kite.trade/forum/discussion/6778/nifty-bank-nifty-trading-symbol-for-jan-2020-weekly-contracts
    https://kite.trade/forum/discussion/5574/change-in-format-of-weekly-options-instruments
    https://kite.trade/forum/discussion/8981/weekly-option-contract-trading-symbol
    :param tradingsymbol:
    :param strike:
    :param dt_exp:
    :param opt_type:
    :return:
    """
    KNOWN_SYMBOLS = {
        'NIFTY 50': 'NIFTY',
        'NIFTY BANK': 'BANKNIFTY'
    }

    # Monthly mappings for option tradingsymbols as found in kite forums
    MONTHLY_MAPPING = {
        "01": "1",
        "02": "2",
        "03": "3",
        "04": "4",
        "05": "5",
        "06": "6",
        "07": "7",
        "08": "8",
        "09": "9",
        "10": "O",
        "11": "N",
        "12": "D",
    }

    assert (opt_type in ['PE', 'CE'])
    assert (exp_type in ['Weekly', 'Monthly'])

    tradingsymbol = KNOWN_SYMBOLS.get(tradingsymbol, tradingsymbol)

    # If the tradingsymbol already is OPT symbol, return as is
    if tradingsymbol[-2:] == 'PE' or tradingsymbol[-2:] == 'CE':
        return tradingsymbol
    else:
        spot_name = re.sub('\d{2}[A-Z]{3}\d+[A-Z]{2}', '', tradingsymbol)  # trimming with monthly regex
        if spot_name.__len__() == tradingsymbol.__len__():
            spot_name = re.sub('\d{2}[1-9OND]\d{2}\d+[CP]E', '', tradingsymbol)  # trimming with weekly regex

    if exp_type == 'Weekly':
        return f"{spot_name}{dt_exp.strftime('%y')}{MONTHLY_MAPPING[dt_exp.strftime('%m')]}{dt_exp.strftime('%d')}{strike}{opt_type}".upper()
    else:
        # Monthly option tradingsymbols have different format than weekly
        return f"{spot_name}{dt_exp.strftime('%y%b')}{strike}{opt_type}".upper()


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


def get_annualized_dte(dte_seconds):
    """
    Get Annualized DTE
    :param dte_seconds: Days to expiry measured in seconds
    :return: float
    """
    return (((dte_seconds / 60.) / 60.) / 24.) / 365.
