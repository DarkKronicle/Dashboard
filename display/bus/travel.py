from typing import Optional

import aiohttp

from display.api.serialize import ModelList
from display.bus.estimates import Estimates
from display.bus.routes import Routes
from display.bus.storage.estimate import Estimate
from display.bus.storage.route import Route, Stop
from display.bus.vehicles import Vehicles


class TravelHolder:

    def __init__(self):
        self.routes = []
        self.vehicles = []
        self.estimates = []

    async def fetch(self):
        async with aiohttp.ClientSession() as session:
            self.routes = await Routes.refresh(session)
            self.vehicles = await Vehicles.refresh(session)
            self.estimates = await Estimates.refresh(session)

    async def fetch_estimates(self):
        async with aiohttp.ClientSession() as session:
            self.estimates = await Estimates.refresh(session)

    def get_route(self, name) -> Optional[Route]:
        for r in self.routes:
            if r.description == name:
                return r
        return None

    def filter_estimates(self, *, route: Optional[Route] = None, stop: Optional[Stop] = None):
        def check(estimate: Estimate):
            return (route is None or route.route_id == estimate.route_id) and (stop is None or stop.route_stop_id == estimate.stop_id)

        return Estimates(ModelList(list(filter(check, self.estimates))))
