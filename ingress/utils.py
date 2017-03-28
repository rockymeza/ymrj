import enum


class Intent(enum.Enum):
    start_period = 'start_period'
    end_period = 'end_period'
    unknown = 'unknown'


def extract_message_intent(body):
    if '来了' in body:
        return Intent.start_period
    elif '走了' in body:
        return Intent.end_period
    else:
        return Intent.unknown
