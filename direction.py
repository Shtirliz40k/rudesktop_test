import enum


class Direction(enum.Enum):
    TOP = enum.auto()
    BOTTOM = enum.auto()
    RIGHT = enum.auto()
    LEFT = enum.auto()


CLOCKWISE_ROTATION = {
    Direction.TOP: Direction.RIGHT,
    Direction.RIGHT: Direction.BOTTOM,
    Direction.BOTTOM: Direction.LEFT,
    Direction.LEFT: Direction.TOP,
}

COUNTER_CLOCKWISE_ROTATION = {
    Direction.TOP: Direction.LEFT,
    Direction.LEFT: Direction.BOTTOM,
    Direction.BOTTOM: Direction.RIGHT,
    Direction.RIGHT: Direction.TOP,
}
