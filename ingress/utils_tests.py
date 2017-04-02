import datetime

import pytest
from freezegun import freeze_time

from .utils import Intent, extract_message_intent


TODAY = datetime.date(2017, 4, 2)


def test_unknown():
    intent = extract_message_intent('乱七八糟')
    assert intent is None


@pytest.mark.parametrize('test_input,date', [
    ('来了', TODAY),
    ('来啦', TODAY),
    ('昨天来了', TODAY - datetime.timedelta(days=1)),
    ('前天来了', TODAY - datetime.timedelta(days=2)),
    ('7号来的', datetime.date(2017, 3, 7)),
    ('七号来的', datetime.date(2017, 3, 7)),
])
@freeze_time(TODAY)
def test_laile(test_input, date):
    intent = extract_message_intent(test_input)
    assert intent == Intent(
        type='start_period',
        kwargs={
            'start_date': date,
        },
    )


@pytest.mark.parametrize('test_input,date', [
    ('走了', TODAY),
    ('走咯', TODAY),
    ('走啦', TODAY),
    ('三十一日走啦', datetime.date(2017, 3, 31)),
])
@freeze_time(TODAY)
def test_zoule(test_input, date):
    intent = extract_message_intent(test_input)
    assert intent == Intent(
        type='end_period',
        kwargs={
            'end_date': date,
        },
    )
