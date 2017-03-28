import logging

from django.http import HttpResponse, HttpResponseNotFound
from django_twilio.decorators import twilio_view
from django_twilio.request import decompose

from .models import IncomingMessage
from .tasks import process_incoming_message

log = logging.getLogger()


@twilio_view
def receive_twilio_sms(request):
    twilio_req = decompose(request)

    if twilio_req.type != 'message':
        log.warn(
            'Unknown request type %s, from %s (Twilio ID: %s)',
            twilio_req.type, twilio_req.from_, twilio_req.messagesid,
        )
        return HttpResponseNotFound()

    message = IncomingMessage.objects.create(
        twilio_id=twilio_req.messagesid,
        from_number=twilio_req.from_,
        to_number=twilio_req.to,
        body=twilio_req.body,
    )

    process_incoming_message.delay(message.id)

    return HttpResponse(status=204)
