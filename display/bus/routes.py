from typing import Iterator

import aiohttp

from display import config
from display.api.serialize import ModelList
from display.bus.storage.route import Route

routes_url = config['routes_url']


class Routes:

    def __init__(self):
        self.routes: list[Route] = []

    def __iter__(self) -> Iterator[Route]:
        for r in self.routes:
            yield r

    @staticmethod
    async def refresh(session: aiohttp.ClientSession):
        async with session.request('GET', routes_url) as r:
            if r.status != 200:
                print(await r.text())
                return None
            return ModelList(Route.from_kwargs(**v) for v in await r.json(content_type=None))
