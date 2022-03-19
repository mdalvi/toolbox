import calendar
from datetime import date, timedelta


def get_last_day_of_month(year, month, day='Thursday'):
    daysInMonth = calendar.monthrange(year, month)[1]  # Returns (month, numberOfDaysInMonth)
    dt = date(year, month, daysInMonth)

    d = {'Monday': 1, 'Tuesday': 2, 'Wednesday': 3, 'Thursday': 4, 'Friday': 5, 'Saturday': 6, 'Sunday': 7}
    offset = d[day] - dt.isoweekday()
    if offset > 0:
        offset -= 7  # Back up one week if necessary

    dt += timedelta(offset)
    return dt  # date
