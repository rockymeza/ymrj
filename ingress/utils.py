import datetime
import re
from collections import namedtuple

from dateutil.relativedelta import relativedelta

from chinese import CN_DIGITS, cn2int


day_re = re.compile(r'(\d+)(?:日|号)', re.UNICODE)
cn_day_re = re.compile(r'([' + CN_DIGITS + r']{1,3})(?:日|号)', re.UNICODE)


def extract_day(body):
    day_match = day_re.search(body)
    if day_match:
        return int(day_match.group(1))
    cn_day_match = cn_day_re.search(body)
    if cn_day_match:
        return cn2int(cn_day_match.group(1))


def extract_date(body):
    today = datetime.date.today()
    if '昨天' in body:
        return today - datetime.timedelta(days=1)
    elif '前天' in body:
        return today - datetime.timedelta(days=2)

    day = extract_day(body)
    if day is not None:
        date = today
        if today.day < day:
            date -= relativedelta(months=1)
        return date.replace(day=day)
    return today


Intent = namedtuple('Intent', ['type', 'kwargs'])
start_re = re.compile(r'来(?:了|啦|咯|的)', re.UNICODE)
end_re = re.compile(r'走(?:了|啦|咯|的)', re.UNICODE)


def extract_message_intent(body):
    if start_re.search(body):
        return Intent(
            type='start_period',
            kwargs={
                'start_date': extract_date(body),
            },
        )
    elif end_re.search(body):
        return Intent(
            type='end_period',
            kwargs={
                'end_date': extract_date(body),
            },
        )
