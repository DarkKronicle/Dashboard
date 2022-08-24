import re
from datetime import datetime, timedelta
from typing import Optional

from pytz import timezone

UTC = timezone('utc')
MDT = timezone('America/Denver')


def utc_object(time: datetime) -> datetime:
    return UTC.localize(time)


def to_timezone(time: datetime, zone: str) -> datetime:
    return time.astimezone(timezone(zone))


def get_js_time(time: str) -> Optional[datetime]:
    if time is None:
        return None
    matches = re.findall(r'\d+', str(time))
    stamp: int = int(matches[0])
    time: datetime = datetime.fromtimestamp(stamp // 1000)
    if len(matches) > 1:
        # Weird timezone offset
        zone: int = int(matches[1])
        return utc_object(time - timedelta(hours=zone // 100))
    return to_timezone(MDT.localize(time), 'UTC')


def round_time(time_object=None, round_to=30 * 60):
    """
    Round a datetime object to any time lapse in seconds
    dt : datetime.datetime object, default now.
    roundTo : Closest number of seconds to round to, default 1 minute.
    Author: Thierry Husson 2012 - Use it as you want but don't blame me.
    """
    if time_object is None:
        zone = timezone('UTC')
        utc = timezone('UTC')
        time_object = utc.localize(datetime.now())
        time_object = time_object.astimezone(zone)

    stripped_dt = time_object.replace(tzinfo=None, hour=0, minute=0, second=0)
    seconds = (time_object.replace(tzinfo=None) - stripped_dt).seconds
    rounding = (seconds + round_to / 2) // round_to * round_to
    return time_object + timedelta(0, rounding - seconds, -time_object.microsecond)


def get_time_until_minute():
    return 60 - datetime.now().second
