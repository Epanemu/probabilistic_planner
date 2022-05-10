from maze import Tile
from utils import Pos, Dir
import random

class Engine:
    SUCCESS_PROB = 0.7
    DEVIATION_PROB = 0.15

    def __init__(self, maze):
        self.maze = maze
        self.pubs = []

        for y, row in enumerate(maze.tiles):
            for x, tile in enumerate(row):
                if tile == Tile.START:
                    self.start = Pos(x, y)
                if tile == Tile.GOAL:
                    self.goal = Pos(x, y)
                if tile == Tile.PUB:
                    self.pubs.append(Pos(x, y))

    def walk(self, pos, direction):
        """
            Perform probabilistic action, return (/was the action successful?/, reward)
        """
        rand_val = random.uniform(0,1)
        if rand_val < self.SUCCESS_PROB:
            true_dir = direction
        elif rand_val < self.SUCCESS_PROB + self.DEVIATION_PROB:
            true_dir = direction.shift_left()
        else:
            true_dir = direction.shift_right()

        reward = self.determinitstic_walk(pos, true_dir)

        return true_dir == direction, reward

    def determinitstic_walk(self, pos, direction):
        """
            Perform deterministic action, return reward
        """

        if direction in self.available_directions(pos):
            pos.move(direction)

            if pos == self.goal:
                return 200
            elif pos in self.pubs:
                return -50
            else:
                return -1
        else:
            # if staying at the same position, always -1  <- this seems to make a difference, if -50 or -1 on staying in a pub
            return -1

    def available_directions(self, pos):
        """
            Get available actions
        """
        res = []
        for direction in Dir:
            d_pos = pos.copy()
            d_pos.move(direction)
            if self.maze.walkable(d_pos):
                res.append(direction)
        return res

    def get_reachable(self):
        """
            Returns list of all positions that are reachable
        """
        reachable = set()

        reachable.add(self.start)
        q = [self.start]
        while len(q) > 0:
            pos = q.pop(0)
            for n in pos.four_neighbourhood():
                if self.maze.walkable(n) and n not in reachable:
                    reachable.add(n)
                    q.append(n)

        return reachable
