from enum import Enum


class Position(Enum):

    BOTTOM_LEFT = (-1, -1)
    BOTTOM_MIDDLE = (0, -1)
    BOTTOM_RIGHT = (1, -1)
    MIDDLE_LEFT = (-1, 0)
    MIDDLE_MIDDLE = (0, 0)
    MIDDLE_RIGHT = (1, 0)
    TOP_LEFT = (-1, 1)
    TOP_MIDDLE = (0, 1)
    TOP_RIGHT = (1, 1)

    def get_xy(self, x, y, width, height, *, y_is_top=True) -> tuple[float, float]:
        # :o
        dirs = self.name.split('_')
        x_axis = dirs[1]
        y_axis = dirs[0]
        x_pos = 0
        match x_axis:
            case 'LEFT':
                x_pos = 0
            case 'RIGHT':
                x_pos = width
            case 'MIDDLE':
                x_pos = width / 2
        y_pos = 0
        match y_axis:
            case 'TOP':
                y_pos = 0 if y_is_top else height
            case 'BOTTOM':
                y_pos = height if y_is_top else 0
            case 'MIDDLE':
                y_pos = height / 2
        return x + x_pos, y + y_pos

