from enum import Enum

class Dir(Enum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3

    def shift_right(self):
        """
            Return direction shifted to the right from the self one
        """
        if self == Dir.NORTH:
            return Dir.EAST
        elif self == Dir.EAST:
            return Dir.SOUTH
        elif self == Dir.SOUTH:
            return Dir.WEST
        elif self == Dir.WEST:
            return Dir.NORTH

    def shift_left(self):
        """
            Return direction shifted to the left from the self one
        """
        if self == Dir.NORTH:
            return Dir.WEST
        elif self == Dir.EAST:
            return Dir.NORTH
        elif self == Dir.SOUTH:
            return Dir.EAST
        elif self == Dir.WEST:
            return Dir.SOUTH

    def __str__(self):
        if self == Dir.NORTH:
            return "▲"
        elif self == Dir.EAST:
            return "►"
        elif self == Dir.SOUTH:
            return "▼"
        elif self == Dir.WEST:
            return "◄"

    def __repr__(self):
        return str(self)

class Pos:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def move(self, direction):
        """
            Change this position (in place!) according to the direction
        """
        if direction == Dir.NORTH:
            self.y -= 1
        elif direction == Dir.EAST:
            self.x += 1
        elif direction == Dir.SOUTH:
            self.y += 1
        elif direction == Dir.WEST:
            self.x -= 1

    def copy(self):
        return Pos(self.x, self.y)

    def four_neighbourhood(self):
        return [Pos(self.x+1, self.y), Pos(self.x-1, self.y), Pos(self.x, self.y+1), Pos(self.x, self.y-1)]

    def __str__(self):
        return f"Pos({self.x}, {self.y})"

    def __repr__(self):
        return str(self)

    def __lt__(self, other):
        if self.y < other.y:
            return True
        return self.x < other.x

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))
