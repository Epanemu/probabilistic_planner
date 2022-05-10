from strategy import Strategy
from utils import Dir
from heapq import *

class ValueIteration(Strategy):
    """
        Represents Value Iteration method of getting the optimal policy
    """

    def __init__(self, engine, gamma, lim_residual=1e-5):
        assert gamma < 1 and gamma >= 0, f"gamma should be in [0,1), not {gamma}"

        self.gamma = gamma
        self.lim_residual = lim_residual
        # there is an unreachable position (30, 6) in maze 51-A2 (and possibly some other) -> init all to 0 before proper initialization
        self.V = {}
        for s in engine.get_reachable():
            self.V[s] = 0
        self.__init_V(engine)
        self.compute_V(engine)

    def __init_V(self, engine):
        """
            initialize the V values to the reward, if the actions were deterministic
        """

        closed = set()
        q = []
        heappush(q, (0, engine.goal))
        while len(q) > 0:
            cost, pos = heappop(q)
            if pos in closed:
                continue

            closed.add(pos)
            self.V[pos] = 200 - cost

            for direction in engine.available_directions(pos):
                n_pos = pos.copy()
                reward = engine.determinitstic_walk(n_pos, direction)
                if n_pos not in closed:
                    n_cost = cost + -reward
                    heappush(q, (n_cost, n_pos))
        self.V[engine.goal] = 0

    def compute_V(self, engine):
        """
            Perform the value iteration and create the policy
        """
        states = engine.get_reachable()

        # for a potential spedup, compute all static values only once, initialize V
        actions = {}
        rewards = {}
        next_state = {}
        for state in states:
            actions[state] = list(Dir)
            for action in actions[state]:
                n_state = state.copy()
                rewards[state, action] = engine.determinitstic_walk(n_state, action)
                next_state[state, action] = n_state

        max_residual = self.lim_residual+1
        while max_residual > self.lim_residual:
        # for k in range(engine.maze.h * engine.maze.w):
            max_residual = 0
            V_next = {}
            for state in states:
                if state == engine.goal:
                    V_next[state] = 0
                    continue
                max_val = float("-inf")
                for action in actions[state]:
                    val = engine.SUCCESS_PROB * (rewards[state, action] + self.gamma * self.V[next_state[state, action]])
                    l_action = action.shift_left()
                    val += engine.DEVIATION_PROB * (rewards[state, l_action] + self.gamma * self.V[next_state[state, l_action]])
                    r_action = action.shift_right()
                    val += engine.DEVIATION_PROB * (rewards[state, r_action] + self.gamma * self.V[next_state[state, r_action]])
                    if val > max_val:
                        max_val = val
                    # if state == engine.start:
                    #     print(action, val)
                V_next[state] = max_val
                max_residual = max(max_residual, abs(self.V[state] - max_val))
                # if state == engine.start and self.V[state] > self.V[next_state[state, Dir.SOUTH]]:
                #     print(self.V[state])
                #     print(self.V[next_state[state, Dir.SOUTH]])

            self.V = V_next
            # print(k, "/", engine.maze.h * engine.maze.w)
            # print(max_residual)
            # self.show_value(engine.maze)
            # print()

        self.policy = {}
        for state in states:
            max_val = float("-inf")
            max_action = None
            for action in actions[state]:
                val = engine.SUCCESS_PROB * (rewards[state, action] + self.gamma * self.V[next_state[state, action]])
                l_action = action.shift_left()
                val += engine.DEVIATION_PROB * (rewards[state, l_action] + self.gamma * self.V[next_state[state, l_action]])
                r_action = action.shift_right()
                val += engine.DEVIATION_PROB * (rewards[state, r_action] + self.gamma * self.V[next_state[state, r_action]])
                if val > max_val:
                    max_val = val
                    max_action = action
            self.policy[state] = max_action

    def show_policy(self, engine):
        policy_map = [[None]*engine.maze.w for _ in range(engine.maze.h)]
        for state in engine.get_reachable():
            policy_map[state.y][state.x] = self.policy[state]
        print(engine.maze.to_str(policy_map))

    def show_value(self, engine):
        value_map = [[None]*engine.maze.w for _ in range(engine.maze.h)]
        for state in engine.get_reachable():
            value_map[state.y][state.x] = round(self.V[state])
        print(engine.maze.to_str(value_map))

    def next_move(self, engine, pos):
        """
            Chooses the next action, based on the position in the maze
        """
        return self.policy[pos]
