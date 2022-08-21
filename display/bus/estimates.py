import aiohttp

from display import config
from display.api.serialize import ModelList
from display.bus.storage.estimate import Estimate


eta_url = config['eta_url']


class Estimates:

    def __init__(self, estimates: list[Estimate]):
        self.estimates: list[Estimate] = [e for e in estimates if len(e.times) > 0]

    def __iter__(self):
        for e in self.estimates:
            yield e

    @staticmethod
    async def refresh(session: aiohttp.ClientSession):
        async with session.request('GET', eta_url) as r:
            if r.status != 200:
                print(await r.text())
                return None
            return ModelList(Estimate.from_kwargs(**v) for v in await r.json(content_type=None))

    def get_by_closest(self):
        return sorted(self.estimates, key=lambda e: e.times[0])
