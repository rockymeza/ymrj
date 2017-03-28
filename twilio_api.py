from django.conf import settings
from django_twilio.client import twilio_client
from twilio.exceptions import TwilioException


def send_sms(to, body):
    options = {}

    if settings.TWILIO_MESSAGING_SERVICE_ID:
        options['messaging_service_sid'] = settings.TWILIO_MESSAGING_SERVICE_ID
    else:
        options['from_'] = settings.TWILIO_FROM_NUMBER

    try:
        return twilio_client.messages.create(
            to=to,
            body=body,
            **options
        )
    except TwilioException as e:
        print(e)
