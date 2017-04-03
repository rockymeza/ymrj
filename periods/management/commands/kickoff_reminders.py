import logging

from django.core.management.base import BaseCommand

from ..models import Period
from ..tasks import notify_upcoming_period

log = logging.getLogger()


class Command(BaseCommand):
    help = 'Kicks off tasks for notifying users of upcoming periods'

    def handle(self, *args, **options):
        log.info('kickoff_reminders invoked')
        all_phone_numbers = Period.objects.values_list(
            'phone_number',
            flat=True,
        ).distinct()
        for number in all_phone_numbers:
            notify_upcoming_period.delay(number.as_e164)
