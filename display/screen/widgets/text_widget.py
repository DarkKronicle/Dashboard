from typing import Union

import pygame

from display.api.color import Color
from display.screen.position import Position
from display.screen.widget import Widget


class TextWidget(Widget):

    def __init__(
            self,
            screen,
            x: int,
            y: int,
            width: int,
            height: int,
            text: str = '',
            *,
            font_name: str = 'IBMPlex',
            font_size: int = 30,
            bold: bool = False,
            italic: bool = False,
            color: Union[str, Color] = None,
            position: Position = Position.TOP_LEFT,
    ):
        super().__init__(screen, x, y, width, height)
        self.text = text
        if color is None:
            self.color = Color(1, 1, 1)
        else:
            self.color = color if isinstance(color, Color) else Color.from_string(str(color))
        self.font_name = font_name
        self.font_size = font_size
        self.bold = bold
        self.italic = italic
        self.position = position

    def get_text(self) -> str:
        return self.text

    def get_xy(self, font: pygame.freetype.Font, text: str) -> tuple[int, int]:
        rect = font.get_rect(text)
        text_w = rect.width
        text_h = rect.height
        tup = self.position.get_xy(self.x, self.y + text_h, self.width - text_w, self.height - text_h)
        return int(tup[0]), int(tup[1])

    def get_font(self) -> pygame.freetype.Font:
        return self.screen.ui_manager.ui_theme.font_dict.find_font(
            font_name=self.font_name, font_size=self.font_size, bold=self.bold, italic=self.italic
        )

    def get_color(self) -> Color:
        return self.color

    def render(self) -> None:
        font = self.get_font()
        text = self.get_text()
        font.render_to(self.screen.screen, self.get_xy(font, text), text, self.get_color().int_tuple)
