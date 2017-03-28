import datetime
import logging

from celery import shared_task

from egress.tasks import send_sms
from periods.tasks import start_period, end_period

from .models import IncomingMessage
from .utils import Intent, extract_message_intent

log = logging.getLogger()


@shared_task
def process_incoming_message(id):
    message = IncomingMessage.objects.get(id=id)
    intent = extract_message_intent(message.body)

    if intent is Intent.start_period:
        start_period.delay(
            number=message.from_number.as_e164,
            start_date=datetime.date.today(),
        )
    elif intent is Intent.end_period:
        end_period.delay(
            number=message.from_number.as_e164,
            end_date=datetime.date.today(),
        )
    else:
        send_sms.delay(
            number=message.from_number.as_e164,
            body='我看不懂。',
        )
