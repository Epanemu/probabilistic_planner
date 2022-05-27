from stat_tester import simulate_sequence
import pickle
import seaborn as sns
import numpy as np
import matplotlib.pylab as plt
from matplotlib.colors import LogNorm

def show_path(engine, strategy):
    path, rew, missteps = simulate_sequence(engine, strategy)

    path_map = [[None]*engine.maze.w for _ in range(engine.maze.h)]
    for i, (pos, direction) in enumerate(path):
        path_map[pos.y][pos.x] = str(i%100) + str(direction)
    print(f"Path was {len(path)} steps long, Pepa made {sum(missteps)} total missteps ({sum(missteps)/len(path)*100:.2f}%)")
    print("Total reward:", sum(rew))
    print(engine.maze.to_str(path_map))

def load_data(algos, sizes, types):
    rewards = {}
    times = {}
    tot_times = {}
    for a in algos:
        rewards[a] = {}
        times[a] = {}
        tot_times[a] = {}
        for s in sizes:
            rewards[a][s] = {}
            times[a][s] = {}
            with open(f"results/{a}_{s}", "rb") as f:
                vals = pickle.load(f)
                for t in types:
                    rewards[a][s][t] = vals[f"maze-{s}-{t}.txt"]
                    times[a][s][t] = vals[f"maze-{s}-{t}.txt_process_time"]
                tot_times[a][s] = vals[f"total_time"]

    return rewards, times, tot_times

def plot_time_grid(algos, sizes, types, times, rewards):
    plt.style.use("seaborn")

    plt.figure(figsize=[7*len(algos),6])
    plt.suptitle("Comparison of average (run)time spent on solving a maze (in ms)")
    for k, a in enumerate(algos):
        plt.subplot(1,len(algos),k+1)
        time_mat = np.zeros((5,5))
        for i, s in enumerate(sizes):
            for j, t in enumerate(types):
                time_mat[i,j] = times[a][s][t]/len(rewards[a][s][t])*1000

        heat_map = sns.heatmap(time_mat, linewidth=1, annot= True, norm=LogNorm(), xticklabels=types, yticklabels=sizes)
        plt.xlabel('TYPE')
        plt.ylabel('SIZE')
        plt.title(f"{a}")
    plt.show()

def show_boxplot_for_type(algos, sizes, types, rewards, t, excluded_sizes=[], excluded_algs=[]):
    plt.figure(figsize=[7*len(algos),6])
    rews = []
    ticks = []
    for s in filter(lambda s: s not in excluded_sizes, sizes):
        for a in filter(lambda a: a not in excluded_algs, algos):
            rews.append(np.array(rewards[a][s][t]))
            ticks.append(f"{a}\n{s} x {s}")

    plt.boxplot(rews)
    plt.xticks(range(1, len(rews)+1), ticks)
    plt.ylabel('Reward')
    plt.title(f"Average rewards on mazes of type {t}"
              + (f" without sizes {', '.join(excluded_sizes)}" if len(excluded_sizes) > 0 else "")
              + (f" without algorithms {', '.join(excluded_algs)}" if len(excluded_algs) > 0 else "")
             )
    plt.show()


def avg_diff(algos, sizes, types, rewards, diff_from, diff_from_name):
    print(f"Differences of average rewards compared to {diff_from_name}:")
    print()
    for a in algos:
        if a != diff_from:
            print(a)
            print(" "*13, end="")
            for t in types:
                print(t.ljust(10), end="")
            print()
            for s in sizes:
                print(f"{s}x{s}:".ljust(8), end="")
                for t in types:
                    mean_diff = np.mean(rewards[diff_from][s][t]) - np.mean(rewards[a][s][t])
                    print(f"{mean_diff:.2f}".rjust(10), end="")
                print()
            print()


def rel_diff(algos, sizes, types, rewards, rel_to, rel_to_name):
    print(f"Relative diffferences of average rewards compared to {rel_to_name}:")
    print()
    for a in algos:
        if a != rel_to:
            tot_coef = 0
            averages = {}
            print(a)
            print(" "*13, end="")
            for t in types:
                averages[t] = 0
                print(t.ljust(8), end="")
            print("Average")
            for s in sizes:
                average = 0
                print(f"{s}x{s}:".ljust(8), end="")
                for t in types:
                    # reverse and shift by 200, the upper bound, to make the numbers comparable
                    mean_a = 200 - np.mean(rewards[a][s][t])
                    mean_rel = 200 - np.mean(rewards[rel_to][s][t])
                    mean_diff = mean_a - mean_rel
                    mean_coef = mean_diff / mean_rel
                    print(f"{mean_coef:.3f}".rjust(8), end="")
                    tot_coef += mean_coef
                    averages[t] += mean_coef
                    average += mean_coef
                print("  | ",f"{average/len(types):.3f}".rjust(6), end="")
                print()
            print("-"*60)
            print("Average ", end="")
            for t in types:
                print(f"{averages[t]/len(sizes):.3f}".rjust(8), end="")
            print()
            print(f"In total, the average relative difference is {tot_coef/(len(types)*len(sizes)):.3f}")
            print()