from strategy import Strategy
from heapq import *
from utils import Dir
import numpy as np

class Node:
    def __init__(self, pos, in_action, n_vis=0, value=0, c=1):
        self.pos = pos
        self.in_action = in_action
        self.n_vis = n_vis
        self.value = value
        self.c = c

        self.tried_dirs = []
        self.next = {d:[] for d in Dir}

    def best_action(self):
        """
            Get the best action using the UCT formula
        """
        max_a = None
        max_val = -np.inf
        for a in self.tried_dirs:
            visits = sum(map(lambda n: n.n_vis, self.next[a]))
            value_sum = sum(map(lambda n: n.value, self.next[a]))

            val = value_sum / visits + self.c * np.sqrt(2 * np.log(self.n_vis) / visits)
            if val > max_val:
                max_val = val
                max_a = a
        return max_a


    def __hash__(self):
        return hash((self.pos, self.in_action))

    def __eq__(self, o):
        return self.pos == o.pos and \
            self.in_action == o.in_action


class MCTS(Strategy):
    def __init__(self, engine, n_expansions=20):
        self.rollout = self.__precomp_rollout(engine)
        self.n_expansions = n_expansions

    def __precomp_rollout(self, engine):
        """
            Precompute the rollout values as rewards of positions if the actions were deterministic
            Very similar function used for initializing V values in VI
        """

        rollout = {}
        closed = set()
        q = []
        heappush(q, (0, engine.goal))
        while len(q) > 0:
            cost, pos = heappop(q)
            if pos in closed:
                continue

            closed.add(pos)
            rollout[pos] = 200 - cost

            for direction in engine.available_directions(pos):
                n_pos = pos.copy()
                reward = engine.determinitstic_walk(n_pos, direction)
                if n_pos not in closed:
                    n_cost = cost + -reward
                    heappush(q, (n_cost, n_pos))
        rollout[engine.goal] = 200
        return rollout

    def next_move(self, engine, pos):
        """
            makes set number of expansions (in the constructor)
            decides which action is the best
        """
        graph = Node(pos, None)

        for _ in range(self.n_expansions):
            n, p = self.__select(graph, engine) # select and expand
            delta = self.rollout[n.pos] # rollout
            self.__backup(p+[n], delta) # backup

        # print(graph.next)
        # print(graph.best_action())
        return graph.best_action()

    def __select(self, v, engine):
        parent_list = []
        while v.pos != engine.goal:
            parent_list.append(v)
            if len(v.tried_dirs) < 4:
                n = self.__expand(v, engine)
                return n, parent_list
            else:
                a = v.best_action()
                nextpos = v.pos.copy()
                engine.walk(nextpos, a)
                n = Node(nextpos, a)
                #  if does not yet exist, treat it like expansion
                if n not in v.next[a]:
                    v.next[a].append(n)
                    return n, parent_list

                # if exists continue there
                for v_n in v.next[a]:
                    if n == v_n:
                        v = v_n
                        break

        return v, parent_list

    def __expand(self, v, engine):
        all_dirs = [d for d in Dir]
        valid_dirs = list(filter(lambda d: d not in v.tried_dirs, all_dirs))
        action = np.random.choice(valid_dirs)

        nextpos = v.pos.copy()
        engine.walk(nextpos, action)
        n = Node(nextpos, action) # visits and value are set later.
        v.next[action].append(n)
        v.tried_dirs.append(action)

        return n

    def __backup(self, node_list, n_val):
        for n in node_list:
            n.n_vis += 1
            n.value += n_val

