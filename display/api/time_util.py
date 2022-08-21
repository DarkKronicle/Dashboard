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
