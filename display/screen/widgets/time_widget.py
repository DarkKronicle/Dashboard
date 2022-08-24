from datetime import datetime

import pygame

from display.screen.screen import Screen
from display.screen.widget import Widget
from display.api import time_util


class TimeWidget(Widget):

    def __init__(self, screen: Screen, x, y, width, height):
        super().__init__(screen, x, y, width, height)

    async def add(self) -> None:
        pass

    async def remove(self) -> None:
        pass

    def render(self):
        time = time_util.utc_object(datetime.utcnow())
        time = time_util.to_timezone(time, 'America/Denver')
        font: pygame.font = self.screen.ui_manager.get_theme().get_font_dictionary().find_font(font_name='IBMPlex', font_size=50, bold=False, italic=False)
        font.render_to(self.screen.screen, (self.x, self.y + self.height), time.strftime('%H:%M:%S'), (255, 255, 255))
