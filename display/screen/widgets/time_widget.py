from datetime import datetime

from display.screen.position import Position
from display.screen.screen import Screen
from display.api import time_util
from display.screen.widgets.text_widget import TextWidget


class TimeWidget(TextWidget):

    def __init__(self, screen: Screen, x, y, width, height, position: Position = Position.MIDDLE_MIDDLE):
        super().__init__(screen, x, y, width, height, font_name='IBMPlex', font_size=50, position=position)

    def get_text(self):
        time = time_util.utc_object(datetime.utcnow())
        time = time_util.to_timezone(time, 'America/Denver')
        return time.strftime('%H:%M:%S')
