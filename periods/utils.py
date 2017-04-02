import datetime
import itertools

from .models import Period

# https://www.womenshealth.gov/a-z-topics/menstruation-and-menstrual-cycle
AVERAGE_MENSTRUAL_CYCLE = datetime.timedelta(days=28)


def avg(lst):
    length = 0
    total = 0
    for item in lst:
        total += item
        length += 1
    return total / length


def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    # https://docs.python.org/3/library/itertools.html?highlight=itertools#module-itertools
    a, b = itertools.tee(iterable)
    next(b, None)
    return zip(a, b)


def calculate_next_period(phone_number):
    latest_periods = Period.objects.filter(phone_number=phone_number)[:3]
    if len(latest_periods) == 0:
        return None

    if len(latest_periods) == 1:
        average_period_length = AVERAGE_MENSTRUAL_CYCLE
    else:
        deltas = (
            (a - b).days
            for a, b in pairwise([
                    period.start_date
                    for period in latest_periods
            ])
        )
        average_period_length = datetime.timedelta(days=round(avg(deltas)))
    return latest_periods[0].start_date + average_period_length
