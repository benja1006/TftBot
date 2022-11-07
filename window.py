from dataclasses import dataclass


@dataclass
class Window:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
