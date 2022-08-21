import aiohttp

from display import config
from display.api.serialize import ModelList
from display.bus.storage.vehicle import Vehicle


vehicle_url = config['vehicle_url']


class Vehicles:

    def __init__(self):
        self.vehicles: list[Vehicle] = []

    def __iter__(self):
        for v in self.vehicles:
            yield v

    @staticmethod
    async def refresh(session: aiohttp.ClientSession):
        async with session.request('GET', vehicle_url) as r:
            if r.status != 200:
                print(await r.text())
                return None
            return ModelList(Vehicle.from_kwargs(**v) for v in await r.json(content_type=None))
