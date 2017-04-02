import datetime

import pytest
from freezegun import freeze_time

from .models import Period
from .utils import calculate_next_period


TODAY = datetime.date(2017, 4, 2)
PHONE_NUMBER = '+15551234567'


def PeriodFactory(**kwargs):
    params = {
        'phone_number': PHONE_NUMBER,
        **kwargs
    }
    return Period.objects.create(**params)


@pytest.mark.django_db
def test_calculate_next_period_no_periods():
    assert calculate_next_period(PHONE_NUMBER) is None


@pytest.mark.django_db
@freeze_time(TODAY)
def test_calculate_next_period_one_period():
    Period.objects.create(
        phone_number=PHONE_NUMBER,
        start_date=datetime.date(2017, 3, 25),
    )
    assert calculate_next_period(PHONE_NUMBER) == datetime.date(2017, 4, 22)


@pytest.mark.django_db
@freeze_time(TODAY)
def test_calculate_next_period_three_periods():
    # 30 day average
    PeriodFactory(start_date=datetime.date(2017, 1, 24))
    PeriodFactory(start_date=datetime.date(2017, 2, 23))
    PeriodFactory(start_date=datetime.date(2017, 3, 25))
    assert calculate_next_period('+15551234567') == datetime.date(2017, 4, 24)
