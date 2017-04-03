import datetime
import logging

from celery import shared_task
from dateutil.parser import parse

from egress.tasks import send_sms

from .models import Period, Reminder
from .utils import calculate_next_period

log = logging.getLogger()


START_PERIOD_BODY = """
我来了呀！（{start_date}）
""".strip()


@shared_task
def start_period(number, start_date):
    log.info('start_period %s %s', number, start_date)
    start_date = parse(start_date).date()
    Period.objects.create(
        phone_number=number,
        start_date=start_date,
    )
    send_sms.delay(
        number=number,
        body=START_PERIOD_BODY.format(
            start_date=start_date,
        ),
    )


END_PERIOD_BODY = """
拜拜！（{end_date}）
""".strip()


@shared_task
def end_period(number, end_date):
    log.info('end_period %s %s', number, end_date)
    end_date = parse(end_date).date()
    try:
        period = Period.objects.active().filter(phone_number=number)[0]
    except IndexError:
        send_sms.delay(
            number=number,
            body='怎么还没来就走了呢？',
        )
    else:
        period.finish(end_date)
        send_sms.delay(
            number=number,
            body=END_PERIOD_BODY.format(
                end_date=end_date,
            ),
        )


REMINDER_TRESHOLD_TOO_LATE = datetime.timedelta(days=-1)
REMINDER_TRESHOLD = datetime.timedelta(days=2)
REMINDER_BODY = """
我大概{next_period}要到啦。准备接驾！
""".strip()


@shared_task
def notify_upcoming_period(number):
    next_period = calculate_next_period(number)
    delta = next_period - datetime.date.today()
    if REMINDER_TRESHOLD_TOO_LATE < delta <= REMINDER_TRESHOLD:
        _, created = Reminder.objects.get_or_create(
            phone_number=number,
            estimated_start_date=next_period,
        )
        if created:
            send_sms.delay(
                number=number,
                body=REMINDER_BODY.format(
                    next_period=next_period,
                ),
            )
