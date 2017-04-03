import datetime
from unittest.mock import patch

import pytest
from freezegun import freeze_time

from .factories import PHONE_NUMBER, PeriodFactory
from .tasks import notify_upcoming_period


@pytest.mark.django_db
@patch('periods.tasks.send_sms.delay')
def test_notify_upcoming_period_works(send_sms_delay):
    PeriodFactory(start_date=datetime.date(2017, 1, 24))
    PeriodFactory(start_date=datetime.date(2017, 2, 23))
    PeriodFactory(start_date=datetime.date(2017, 3, 25))

    with freeze_time('2017-04-22'):
        notify_upcoming_period(PHONE_NUMBER)
        send_sms_delay.assert_called_with(
            number=PHONE_NUMBER,
            body='我大概2017-04-24要到啦。准备接驾！',
        )
        send_sms_delay.reset_mock()


@pytest.mark.django_db
@patch('periods.tasks.send_sms.delay')
def test_notify_upcoming_period_doesnt_notify_too_early(send_sms_delay):
    PeriodFactory(start_date=datetime.date(2017, 1, 24))
    PeriodFactory(start_date=datetime.date(2017, 2, 23))
    PeriodFactory(start_date=datetime.date(2017, 3, 25))

    with freeze_time('2017-03-26'):
        notify_upcoming_period(PHONE_NUMBER)
        send_sms_delay.assert_not_called()

    with freeze_time('2017-04-20'):
        notify_upcoming_period(PHONE_NUMBER)
        send_sms_delay.assert_not_called()

    with freeze_time('2017-04-21'):
        notify_upcoming_period(PHONE_NUMBER)
        send_sms_delay.assert_not_called()


@pytest.mark.django_db
@patch('periods.tasks.send_sms.delay')
def test_notify_upcoming_period_doesnt_notify_twice(send_sms_delay):
    PeriodFactory(start_date=datetime.date(2017, 1, 24))
    PeriodFactory(start_date=datetime.date(2017, 2, 23))
    PeriodFactory(start_date=datetime.date(2017, 3, 25))

    with freeze_time('2017-04-22'):
        notify_upcoming_period(PHONE_NUMBER)
        send_sms_delay.assert_called_with(
            number=PHONE_NUMBER,
            body='我大概2017-04-24要到啦。准备接驾！',
        )
        send_sms_delay.reset_mock()

    with freeze_time('2017-04-23'):
        notify_upcoming_period(PHONE_NUMBER)
        send_sms_delay.assert_not_called()


@pytest.mark.django_db
@patch('periods.tasks.send_sms.delay')
def test_notify_upcoming_period_will_notify_if_original_missed(send_sms_delay):
    PeriodFactory(start_date=datetime.date(2017, 1, 24))
    PeriodFactory(start_date=datetime.date(2017, 2, 23))
    PeriodFactory(start_date=datetime.date(2017, 3, 25))

    with freeze_time('2017-04-22'):
        # cron job failed on this day
        pass

    with freeze_time('2017-04-23'):
        notify_upcoming_period(PHONE_NUMBER)
        send_sms_delay.assert_called_with(
            number=PHONE_NUMBER,
            body='我大概2017-04-24要到啦。准备接驾！',
        )


@pytest.mark.django_db
@patch('periods.tasks.send_sms.delay')
def test_notify_upcoming_period_doesnt_notify_if_past(send_sms_delay):
    PeriodFactory(start_date=datetime.date(2017, 1, 24))
    PeriodFactory(start_date=datetime.date(2017, 2, 23))
    PeriodFactory(start_date=datetime.date(2017, 3, 25))

    with freeze_time('2017-04-25'):
        notify_upcoming_period(PHONE_NUMBER)
        send_sms_delay.assert_not_called()
