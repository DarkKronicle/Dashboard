from pathlib import Path
from typing import Union

import pygame

from display.screen.screen import Screen
from display.screen.widget import Widget
from PIL import Image


class Background(Widget):

    def __init__(self, screen: Screen, file: Union[str, Path]):
        super().__init__(screen, 0, 0, screen.screen_size[0], screen.screen_size[1])
        self.file = file if isinstance(file, Path) else Path(str(file))
        self.image = Image.open(str(self.file))
        self.n_frames = self.image.n_frames - 1
        self.current_frame = 0
        self.images = []
        for frame in range(1, self.n_frames + 1):
            self.image.seek(frame)
            image = self.image.copy().resize(self.screen.screen_size)
            self.images.append(pygame.image.fromstring(image.tobytes(), image.size, image.mode))

    def render(self):
        if self.n_frames <= 1:
            image = self.images[0]
        else:
            image = self.images[self.current_frame]
            self.current_frame = (self.current_frame + 1) % self.n_frames
        self.screen.background_surface.blit(image, (0, 0))
