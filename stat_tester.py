import pickle
from engine import Engine
from maze import Maze
import os
import time
import tqdm

def simulate_sequence(engine, strategy):
    path = []
    rewards = []
    missteps = []
    pos = engine.start.copy()
    while pos != engine.goal:
        n_dir = strategy.next_move(engine, pos)
        path.append((pos.copy(), n_dir))
        success, r = engine.walk(pos, n_dir)
        missteps.append(not success)
        rewards.append(r)

        # state_map = [[None]*engine.maze.w for _ in range(engine.maze.h)]
        # state_map[pos.y][pos.x] = "O"
        # print(engine.maze.to_str(state_map))

    return path, rewards, missteps

def multiple_runs(engine, strategy, n_runs):
    tot_rewards = []
    for _ in tqdm.trange(n_runs):
        _, rewards, _ = simulate_sequence(engine, strategy)
        tot_rewards.append(sum(rewards))
        del rewards
    return tot_rewards

def test_some_and_store(out_path, input_path, contains, n_runs, strategy_class, **kwargs):
    """
        Tests given strategy on all inputs containing 'contains' string
    """
    t = time.time()
    results = {}
    for f in os.listdir(input_path):
        if contains in f:
            print("Doing", f)
            maze = Maze(os.path.join(input_path, f))
            engine = Engine(maze)
            strategy = strategy_class(engine, **kwargs)
            print("Strategy done.")
            process_t = time.time()
            results[f] = multiple_runs(engine, strategy, n_runs)
            results[f + "_process_time"] = time.time() - process_t
            del strategy
            print("Testing done.")
    results["total_time"] = time.time() - t

    with open(out_path, 'wb') as f:
        pickle.dump(results, f)