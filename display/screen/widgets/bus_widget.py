from datetime import datetime

import pygame
from pygame_gui.elements import UITextBox

from display.api.color import Color
from display.api.time_util import to_timezone
from display.bus.storage.estimate import EstimatedTime
from display.bus.storage.route import Stop
from display.bus.travel import TravelHolder
from display.screen.screen import Screen
from display.screen.widget import Widget


class BusWidget(Widget):

    def __init__(self, screen: Screen, x, y, width, height):
        super().__init__(screen, x, y, width, height)
        self.estimate_box: UITextBox = None
        self.travel = TravelHolder()

    async def add(self) -> None:
        self.estimate_box = UITextBox(
            '<font face=JetBrainsMono color=regular_text><font color=#E784A2 size=4.5>'
            'Hello there!',
            pygame.Rect(self.x, self.y, self.width, self.height),
            manager=self.screen.ui_manager,
            object_id='#text_box_1',
            anchors={'left': 'left',
                     'right': 'right',
                     'top': 'top',
                     'bottom': 'bottom'}
        )
        await self.travel.fetch()
        self.display_bus_info()

    async def remove(self) -> None:
        self.estimate_box.remove()

    async def on_minute(self, time: datetime) -> None:
        await self.update_bus(time)

    async def update_bus(self, time: datetime):
        time = to_timezone(time, 'America/Denver')
        if 8 <= time.hour <= 17:
            if time.minute % 5 != 0:
                return
        else:
            if time.minute % 20 != 0:
                return
        await self.travel.fetch_estimates()
        self.display_bus_info()

    def display_bus_info(self):
        stop = self.travel.get_stop(name_in=True, name='Heritage')
        times: list[tuple[Stop, EstimatedTime]] = []
        for e in self.travel.filter_estimates(stop=stop).get_by_closest():
            for t in e.times:
                times.append((stop, t))
        times.sort(key=lambda x: x[1])

        estimates = []
        for s, t in times:
            route = self.travel.get_vehicle(t.vehicle_id).get_route(self.travel.routes)
            estimates.append(
                '<font color={color} size=4.5>{0:20} <font color=#FFFFFF>{1}'.format(
                    '[{0}]'.format(route.description),
                    to_timezone(t.estimate_time, 'America/Denver').strftime('%H:%M:%S'),
                    color=Color.from_string(route.map_line_color).blend(Color(1, 1, 1))
                )
            )

        estimates = '<br>'.join(estimates)
        if not estimates:
            estimates = 'No estimates currently!'
        self.estimate_box.set_text('<font face=JetBrainsMono color=regular_text><font color=#E784A2 size=4.5>Heritage Stops:<br>'
                                   '<font color=#FFFFFF size=4>{0}'.format(estimates))

