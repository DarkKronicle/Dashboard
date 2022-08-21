import asyncio
import time
import traceback

from display.api import tasks
from display.api.time_util import to_timezone
from display.bus.travel import TravelHolder

import pygame

from pygame_gui.ui_manager import UIManager
from pygame_gui.elements.ui_text_box import UITextBox
from pygame_gui.core import IncrementalThreadedResourceLoader


class Screen:

    def __init__(self):
        self.estimate_box: UITextBox = None
        self.clock = None
        self.ui_manager = None
        self.background_surface = None
        self.screen = None
        self.screen_size = (800, 600)
        self.travel = TravelHolder()
        self.loop = None
        self.FPS = 5
        self.event_queue = asyncio.Queue()

    def error_thrown(self, error: Exception):
        traceback.print_exception(error)
        self.loop.stop()

    async def pygame_event_loop(self):
        try:
            while True:
                await asyncio.sleep(0)  # allow other tasks to run
                event = pygame.event.poll()
                if event.type != pygame.NOEVENT:
                    await self.event_queue.put(event)
        except Exception as e:
            self.error_thrown(e)

    async def display(self):
        try:
            current_time = 0
            while True:
                last_time, current_time = current_time, time.time()
                await asyncio.sleep(1 / self.FPS - (current_time - last_time))  # tick
                self.ui_manager.update(current_time - last_time)
                self.screen.blit(self.background_surface, (0, 0))
                self.ui_manager.draw_ui(self.screen)
                pygame.display.update()
        except Exception as e:
            self.error_thrown(e)

    async def handle_events(self):
        try:
            await self.setup()
            while True:
                event = await self.event_queue.get()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        break
                if event.type == pygame.QUIT:
                    break
                self.ui_manager.process_events(event)
            asyncio.get_event_loop().stop()
        except Exception as e:
            self.error_thrown(e)

    def start(self):
        self.loop = asyncio.get_event_loop()
        pygame.init()
        pygame.display.set_caption("Dashboard")
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.screen_size = self.screen.get_size()
        self.background_surface = pygame.Surface(self.screen_size)
        self.background_surface.fill(pygame.Color("#000000"))
        loader = IncrementalThreadedResourceLoader()
        self.ui_manager = UIManager(self.screen_size, 'data/themes/theme_1.json', resource_loader=loader)
        self.clock = pygame.time.Clock()
        self.ui_manager.add_font_paths("Montserrat",
                                  "data/fonts/Montserrat-Regular.ttf",
                                  "data/fonts/Montserrat-Bold.ttf",
                                  "data/fonts/Montserrat-Italic.ttf",
                                  "data/fonts/Montserrat-BoldItalic.ttf")

        self.ui_manager.preload_fonts([{'name': 'Montserrat', 'html_size': 4.5, 'style': 'bold'},
                                  {'name': 'Montserrat', 'html_size': 4.5, 'style': 'regular'},
                                  {'name': 'Montserrat', 'html_size': 2, 'style': 'regular'},
                                  {'name': 'Montserrat', 'html_size': 2, 'style': 'italic'},
                                  {'name': 'Montserrat', 'html_size': 6, 'style': 'bold'},
                                  {'name': 'Montserrat', 'html_size': 6, 'style': 'regular'},
                                  {'name': 'Montserrat', 'html_size': 6, 'style': 'bold_italic'},
                                  {'name': 'Montserrat', 'html_size': 4, 'style': 'bold'},
                                  {'name': 'Montserrat', 'html_size': 4, 'style': 'regular'},
                                  {'name': 'Montserrat', 'html_size': 4, 'style': 'italic'},
                                  {'name': 'fira_code', 'html_size': 2, 'style': 'regular'},
                                  {'name': 'fira_code', 'html_size': 2, 'style': 'bold'},
                                  {'name': 'fira_code', 'html_size': 2, 'style': 'bold_italic'}
                                  ])
        loader.start()
        finished_loading = False
        while not finished_loading:
            finished_loading, progress = loader.update()

        pygame_task = self.loop.create_task(self.pygame_event_loop())
        event_task = self.loop.create_task(self.handle_events())
        display_task = self.loop.create_task(self.display())
        try:
            self.loop.run_forever()
        except KeyboardInterrupt:
            pass
        finally:
            pygame_task.cancel()
            event_task.cancel()
            display_task.cancel()

        self.close()

    def close(self):
        self.loop.shutdown_asyncgens()
        self.loop.close()

    async def setup(self):
        await self.travel.fetch()
        self.estimate_box = UITextBox(
            '<font face=Montserrat color=regular_text><font color=#E784A2 size=4.5>'
            'Hello there!',
            pygame.Rect(10, 10, 390, self.screen_size[1] - 20),
            manager=self.ui_manager,
            object_id='#text_box_1',
            anchors={'left': 'left',
                     'right': 'right',
                     'top': 'top',
                     'bottom': 'bottom'}
        )
        self.display_bus_info()
        self.update_bus.start()

    @tasks.loop(minutes=3)
    async def update_bus(self):
        await self.travel.fetch_estimates()
        self.display_bus_info()

    def display_bus_info(self):
        route = self.travel.get_route('Orange')
        estimates = '<br>'.join(
            ['{0}: {1}'.format(
                e.stop_description,
                to_timezone(e.times[0].estimate_time, 'America/Denver') if len(e.times) > 0 else 'None')
                for e in self.travel.filter_estimates(route=route).get_by_closest()
            ]
        )
        if not estimates:
            estimates = 'No estimates currently!'
        self.estimate_box.set_text('<font face=Montserrat color=regular_text><font color=#E784A2 size=4.5>{0}'.format(estimates))
