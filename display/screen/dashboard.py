from display.screen.screen import Screen
from display.screen.widgets.bus_widget import BusWidget


class Dashboard(Screen):

    def __init__(self):
        super().__init__()

    def setup_widgets(self):
        self.widgets.append(BusWidget(self, 10, 10, 330, self.screen_size[1] - 20))


