import asyncio
import time
import traceback
from pathlib import Path

from display.api import tasks
from display.api.time_util import get_time_until_minute, round_time


import pygame

from pygame_gui.ui_manager import UIManager
from pygame_gui.core import IncrementalThreadedResourceLoader

from display.screen.widget import Widget


def get_font_kwargs(path: Path):
    regular_path = None
    bold_path = None
    italic_path = None
    bold_italic_path = None
    for f in path.glob("**/*.ttf"):
        if f.name.endswith('Bold.ttf'):
            bold_path = str(f)
        elif f.name.endswith('Italic.ttf'):
            italic_path = str(f)
        elif f.name.endswith('BoldItalic.ttf'):
            bold_italic_path = str(f)
        elif f.name.endswith('Regular.ttf'):
            regular_path = str(f)
    return {'regular_path': regular_path, 'bold_path': bold_path, 'italic_path': italic_path, 'bold_italic_path': bold_italic_path}


class Screen:

    def __init__(self, *, fps=15):
        self.ui_manager: UIManager = None
        self.background_surface: pygame.Surface = None
        self.screen = None
        self.screen_size = (800, 600)
        self.loop = None
        self.FPS = fps
        self.event_queue = asyncio.Queue()
        self.widgets: list[Widget] = []
        self.time = 0

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
                await asyncio.sleep(1 / self.FPS)  # tick
                self.ui_manager.update(current_time - last_time)
                self.screen.blit(self.background_surface, (0, 0))
                for widget in self.widgets:
                    widget.render()
                self.ui_manager.draw_ui(self.screen)
                pygame.display.update()
                self.tick()
        except Exception as e:
            self.error_thrown(e)

    def tick(self):
        if self.time & 1 == int(time.time()) & 1:
            self.second()

    def second(self):
        for widget in self.widgets:
            widget.second()

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

    def load_font(self, name):
        self.ui_manager.preload_fonts([
            {'name': name, 'html_size': 4.5, 'style': 'bold'},
            {'name': name, 'html_size': 4.5, 'style': 'regular'},
            {'name': name, 'html_size': 2, 'style': 'regular'},
            {'name': name, 'html_size': 2, 'style': 'italic'},
            {'name': name, 'html_size': 6, 'style': 'bold'},
            {'name': name, 'html_size': 6, 'style': 'regular'},
            {'name': name, 'html_size': 6, 'style': 'bold_italic'},
            {'name': name, 'html_size': 4, 'style': 'bold'},
            {'name': name, 'html_size': 4, 'style': 'regular'},
            {'name': name, 'html_size': 4, 'style': 'italic'},
        ])

    def setup_widgets(self):
        raise NotImplementedError()

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
        self.ui_manager.add_font_paths("JetBrainsMono", **get_font_kwargs(Path('./data/fonts/JetBrainsMono')))
        self.ui_manager.add_font_paths("Inter", **get_font_kwargs(Path('./data/fonts/Inter')))
        self.ui_manager.add_font_paths("IBMPlex", **get_font_kwargs(Path('./data/fonts/IBM-Plex-Mono')))

        self.load_font('JetBrainsMono')
        self.load_font('Inter')
        self.load_font('IBMPlex')

        loader.start()
        finished_loading = False
        while not finished_loading:
            finished_loading, progress = loader.update()

        self.setup_widgets()

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
        for widget in self.widgets:
            asyncio.ensure_future(widget.add())
        self.time_loop.start()

    @tasks.loop(minutes=1)
    async def time_loop(self):
        time = round_time(round_to=60)
        for widget in self.widgets:
            try:
                asyncio.ensure_future(widget.on_minute(time))
            except Exception as error:
                traceback.print_exc()

    @tasks.loop(seconds=get_time_until_minute())
    async def setup_loop(self):
        # Probably one of the most hacky ways to get a loop to run every thirty minutes based
        # off of starting on one of them.
        if Screen.first_loop:
            Screen.first_loop = False
            return
        self.time_loop.start()
        self.setup_loop.stop()

    first_loop = True
