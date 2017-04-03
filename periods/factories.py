from .models import Period

PHONE_NUMBER = '+15551234567'


def PeriodFactory(**kwargs):
    params = {
        'phone_number': PHONE_NUMBER,
        **kwargs
    }
    return Period.objects.create(**params)
