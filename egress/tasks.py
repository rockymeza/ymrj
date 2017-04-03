import logging

from celery import shared_task
from django.conf import settings

import twilio_api

from .models import OutgoingMessage

log = logging.getLogger()


@shared_task
def send_sms(number, body):
    if settings.TWILIO_ENABLED:
        log.info('sending sms to %s - %s', number, body)
        twilio_message = twilio_api.send_sms(
            to=number,
            body=body,
        )
        if twilio_message:
            OutgoingMessage.objects.create(
                twilio_id=twilio_message.sid,
                to_number=number,
                body=body,
            )
    else:
        log.warning('Did not send SMS because TWILIO_ENABLED = False')
