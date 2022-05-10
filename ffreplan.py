from heapq import *
import math
from strategy import Strategy

class FFReplan(Strategy):
    def __init__(self, engine):
        self.plan = self.__find_path(engine, engine.start)
        self.pre_pos = engine.goal
        self.c = 0

    def next_move(self, engine, pos):
        """
            Chooses the next action, based on the position in the maze and precomputed plan
            If the position is not in the plan, recompute the plan from current position
        """
        if pos not in self.plan.keys():
            self.plan = self.__find_path(engine, pos.copy())
        return self.plan[pos]

    def __find_path(self, engine, curr_pos):
        # A* with euclidean distance
        closed = set()
        parent = {}
        parent_dirs = {}
        q = []
        heappush(q, (0, 0, curr_pos, None, None))
        while len(q) > 0:
            _, cost, pos, p_pos, direction = heappop(q)
            if pos in closed:
                continue

            closed.add(pos)
            parent[pos] = p_pos
            parent_dirs[pos] = direction

            if pos == engine.goal:
                plan = {}
                while parent[pos] is not None:
                    # each parent also has dir, last pos is goal without dir, thus irrelevant
                    plan[parent[pos]] = parent_dirs[pos]
                    pos = parent[pos]
                return plan


            for direction in engine.available_directions(pos):
                n_pos = pos.copy()
                reward = engine.determinitstic_walk(n_pos, direction)
                if n_pos not in closed:
                    h = math.sqrt((n_pos.x-engine.goal.x)**2 + (n_pos.y-engine.goal.y)**2)
                    n_cost = cost + -reward
                    heappush(q, (n_cost + h, n_cost, n_pos, pos, direction))
