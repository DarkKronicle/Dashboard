from __future__ import annotations
from datetime import datetime
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from display.screen.screen import Screen


class Widget:

    def __init__(self, screen: Screen, x, y, width, height):
        self.screen = screen
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    async def on_minute(self, time: datetime) -> None:
        pass

    async def add(self) -> None:
        raise NotImplementedError()

    async def remove(self) -> None:
        raise NotImplementedError()

    def second(self):
        pass

    def render(self):
        pass

