from dataclasses import dataclass
from datetime import datetime

from display.api.serialize import Model
from display.api.time_util import get_js_time


@dataclass(repr=False)
class Vehicle(Model):

    ground_speed: float
    heading: int
    is_delayed: bool
    is_on_route: bool
    latitude: float
    longitude: float
    name: str
    route_id: int
    seconds: int
    vehicle_id: int
    timestamp: datetime

    def get_route(self, routes):
        for r in routes:
            if r.route_id == self.route_id:
                return r
        return None

    def __post_init__(self):
        self.timestamp = get_js_time(self.timestamp)

