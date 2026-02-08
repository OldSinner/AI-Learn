from dataclasses import dataclass
import enum


class Action(enum.Enum):
    LEFT = 1
    RIGHT = 2
    STRAIGHT = 3


@dataclass
class Vector:
    x: int
    y: int

    def __eq__(self, other):
        if isinstance(other, Vector):
            return self.x == other.x and self.y == other.y
        return False

    def __add__(self, other):
        if isinstance(other, Vector):
            return Vector(self.x + other.x, self.y + other.y)
        return NotImplemented