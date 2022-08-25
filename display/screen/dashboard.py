from display.screen.widgets.background import Background
from display.screen.screen import Screen
from display.screen.widgets.bus_widget import BusWidget
from display.screen.widgets.time_widget import TimeWidget


class Dashboard(Screen):

    def __init__(self):
        super().__init__()

    def setup_widgets(self):
        self.widgets.append(Background(self, 'data/backgrounds/classroom.gif'))
        self.widgets.append(BusWidget(self, 10, 10, 330, self.screen_size[1] - 20))
        self.widgets.append(TimeWidget(self, self.screen_size[0] // 2 - 40, 10, 160, 60))


