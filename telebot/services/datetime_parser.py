from datetime import datetime
from dateparser import parse

def parse_natural_datetime(text: str, base: datetime = None):
    if base is None:
        base = datetime.now()
    return parse(
        text,
        settings={
            'PREFER_DATES_FROM': 'future',
            'RELATIVE_BASE': base,
            'RETURN_AS_TIMEZONE_AWARE': False,
        }
    )