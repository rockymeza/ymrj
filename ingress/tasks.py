import logging

from celery import shared_task

from egress.tasks import send_sms
from periods.tasks import start_period, end_period

from .models import IncomingMessage
from .utils import extract_message_intent

log = logging.getLogger()


@shared_task
def process_incoming_message(id):
    message = IncomingMessage.objects.get(id=id)
    intent = extract_message_intent(message.body)

    if intent.type == 'start_period':
        start_period.delay(
            number=message.from_number.as_e164,
            **intent.kwargs
        )
    elif intent.type == 'end_period':
        end_period.delay(
            number=message.from_number.as_e164,
            **intent.kwargs
        )
    else:
        send_sms.delay(
            number=message.from_number.as_e164,
            body='我看不懂。',
        )
