from dataclasses import dataclass

from display.api.serialize import Model, ModelList
import polyline


@dataclass(repr=False)
class Polyline(Model):

    points: list[tuple[int, int]]

    def __post_init__(self):
        self.points = polyline.decode(self.points)


@dataclass(repr=False)
class Stop(Model):

    address_id: int
    city: str
    state: str
    zip: str
    description: str
    latitude: float
    longitude: float
    line1: str
    line2: str
    order: int
    route_id: int
    route_stop_id: int
    seconds_at_stop: int
    seconds_to_next_stop: int
    sign_verbiage: str


@dataclass(repr=False)
class Route(Model):

    description: str
    eta_type_id:  int
    encoded_polyline: Polyline
    info_text: str
    is_running: bool
    map_latitude: float
    map_line_color: str
    map_longitude: float
    order: int
    route_id: int
    stops: list[Stop]

    def get_vehicle(self, vehicles):
        for v in vehicles:
            if v.route_id == self.route_id:
                return v
        return None

    def __post_init__(self):
        self.encoded_polyline = Polyline.from_kwargs(**{'points': self.encoded_polyline})
        self.stops = ModelList(Stop.from_kwargs(**s) for s in self.stops)
