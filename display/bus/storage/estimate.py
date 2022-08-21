from dataclasses import dataclass
from datetime import datetime

from display.api.serialize import Model, ModelList
from display.api.time_util import get_js_time


@dataclass(repr=False)
class EstimatedTime(Model):

    vehicle_id: int
    estimate_time: datetime
    time: datetime
    is_arriving: bool
    is_departed: bool
    on_time_status: int
    seconds: int
    text: str

    def __post_init__(self):
        self.estimate_time = get_js_time(self.estimate_time)
        self.time = get_js_time(self.time)

    def __gt__(self, other):
        if not isinstance(other, EstimatedTime):
            raise TypeError("Cannot compare EstimatedTime to {0}".format(other))
        return self.estimate_time > other.estimate_time

    def __lt__(self, other):
        if not isinstance(other, EstimatedTime):
            raise TypeError("Cannot compare EstimatedTime to {0}".format(other))
        return self.estimate_time < other.estimate_time


@dataclass(repr=False)
class Estimate(Model):

    color: str
    route_description: str
    route_id: int
    route_stop_id: int
    stop_description: str
    stop_id: int
    times: list[EstimatedTime]

    def get_route(self, routes):
        for r in routes:
            if r.route_id == self.route_id:
                return r
        return None

    def get_first_time(self):
        if len(self.times) > 0:
            return self.times[0]
        return None

    def __post_init__(self):
        self.times = ModelList(EstimatedTime.from_kwargs(**t) for t in self.times)
        self.times.sort()
