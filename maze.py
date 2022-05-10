from enum import Enum
from utils import Pos

black = "\u001b[40m"
red = "\u001b[41m"
green = "\u001b[42m"
yellow = "\u001b[43m"
blue = "\u001b[44m"
magenta = "\u001b[45m"
cyan = "\u001b[46m"
white = "\u001b[47m"
reset = "\u001b[0m"

class Tile(Enum):
    WALL = 1
    EMPTY = 2
    PUB = 3
    START = 4
    GOAL = 5

    @staticmethod
    def from_char(char):
        if char == "#":
            return Tile.WALL
        elif char == " ":
            return Tile.EMPTY
        elif char == "D":
            return Tile.PUB
        elif char == "S":
            return Tile.START
        elif char == "E":
            return Tile.GOAL

    def __str__(self):
        return self.with_elem("  ")

    def with_elem(self, elem):
        """
            Make string of the tile with element inside
        """
        if self == Tile.WALL:
            return white + " "*len(elem) + reset
        elif self == Tile.EMPTY:
            return black + elem + reset
        elif self == Tile.PUB:
            return red + elem + reset
        elif self == Tile.START:
            return blue + elem + reset
        elif self == Tile.GOAL:
            return green + elem + reset

class Maze:
    def __init__(self, in_file):
        with open(in_file, "r") as f:
            self.h, self.w = [int(x) for x in f.readline().split()]
            self.tiles = []

            for r_i in range(self.h):
                self.tiles.append(list(map(lambda char: Tile.from_char(char), f.readline().strip())))

    def walkable(self, pos):
        """
            Returns True if the position can be walked on
        """
        x, y = pos.x, pos.y
        return x >= 0 and x < self.w and y >= 0 and y < self.h and self.tiles[y][x] != Tile.WALL

    def __str__(self):
        res = ""
        for row in self.tiles:
            for t in row:
                res += str(t)
            res += "\n"
        return res

    def to_str(self, elems=None):
        """
            Make a string of the maze, with optional elements shown in the tiles
        """
        if elems is None:
            return str(self)
        max_l = 2 # each tile is wide at least 2
        str_elems = []
        for row in elems:
            str_elems.append([])
            for elem in row:
                # change elements to strings
                str_elem = str(elem) if elem is not None else "  "
                # limit the length
                if len(str_elem) > 4:
                    str_elem = str_elem[:4]
                max_l = max(len(str_elem), max_l)
                str_elems[-1].append(str_elem)

        # add extra space to each element, so they are all the same length
        spaced_elems = []
        for row in str_elems:
            spaced_elems.append([])
            for elem in row:
                diff = max_l - len(elem)
                space_r = diff // 2
                space_l = diff - space_r
                spaced_elem = " " * space_l + elem + " " * space_r
                spaced_elems[-1].append(spaced_elem)

        res = ""
        for i, row in enumerate(self.tiles):
            for j, t in enumerate(row):
                res += t.with_elem(spaced_elems[i][j])
            res += "\n"
        return res

