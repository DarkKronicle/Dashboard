

class Color:

    def __init__(self, r: float, g: float, b: float):
        self.r = min(1.0, max(0.0, r))
        self.g = min(1.0, max(0.0, g))
        self.b = min(1.0, max(0.0, b))

    def blend(self, other, *, percent: float = .5):
        r = self.r * percent + other.r * (1 - percent)
        g = self.g * percent + other.g * (1 - percent)
        b = self.b * percent + other.b * (1 - percent)
        return Color(r, g, b)

    @property
    def int_tuple(self):
        return self.r_int, self.g_int, self.b_int

    @property
    def float_tuple(self):
        return self.r, self.g, self.b

    @property
    def r_int(self):
        return int(self.r * 255)

    @property
    def g_int(self):
        return int(self.g * 255)

    @property
    def b_int(self):
        return int(self.b * 255)

    @property
    def r_str(self):
        return str(hex(self.r_int))[2:]

    @property
    def g_str(self):
        return str(hex(self.g_int))[2:]

    @property
    def b_str(self):
        return str(hex(self.b_int))[2:]

    def __str__(self):
        return '#' + self.r_str + self.g_str + self.b_str

    @classmethod
    def from_int(cls, r, g, b):
        return cls(r / 255, g / 255, b / 255)

    @classmethod
    def from_string(cls, string: str):
        if string.startswith('#'):
            string = string[1:]
        r = int(string[0:2], 16)
        g = int(string[2:4], 16)
        b = int(string[4:6], 16)
        return cls.from_int(r, g, b)
