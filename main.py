#!/usr/bin/env python3

from maze import Maze
from engine import Engine
from ffreplan import FFReplan
from val_iter import ValueIteration
from mcts import MCTS
from stat_tester import simulate_sequence, multiple_runs, test_some_and_store
import sys
import time

def main():
    test_some_and_store("results/ff_replan_7", "dataset-assignment2/data/", "7", 10000, FFReplan)
    test_some_and_store("results/ff_replan_15_2nd", "dataset-assignment2/data/", "15", 10000, FFReplan)
    test_some_and_store("results/ff_replan_25", "dataset-assignment2/data/", "25", 1000, FFReplan)
    test_some_and_store("results/ff_replan_51_2nd", "dataset-assignment2/data/", "51", 100, FFReplan)
    test_some_and_store("results/ff_replan_101_2nd", "dataset-assignment2/data/", "101", 100, FFReplan)

    test_some_and_store("results/val_iter_7", "dataset-assignment2/data/", "7", 10000, ValueIteration, gamma=0.99999, lim_residual=1e-10)
    test_some_and_store("results/val_iter_15", "dataset-assignment2/data/", "15", 10000, ValueIteration, gamma=0.99999, lim_residual=1e-10)
    test_some_and_store("results/val_iter_25", "dataset-assignment2/data/", "25", 10000, ValueIteration, gamma=0.99999, lim_residual=1e-10)
    test_some_and_store("results/val_iter_51", "dataset-assignment2/data/", "51", 10000, ValueIteration, gamma=0.99999, lim_residual=1e-10)
    test_some_and_store("results/val_iter_101", "dataset-assignment2/data/", "101", 10000, ValueIteration, gamma=0.99999, lim_residual=1e-10)

    test_some_and_store("results/mcts_7", "dataset-assignment2/data/", "7", 10000, MCTS, n_expansions=10)
    test_some_and_store("results/mcts_15", "dataset-assignment2/data/", "15", 10000, MCTS, n_expansions=10)
    test_some_and_store("results/mcts_25", "dataset-assignment2/data/", "25", 1000, MCTS, n_expansions=30)
    test_some_and_store("results/mcts_51", "dataset-assignment2/data/", "51", 1000, MCTS, n_expansions=10)
    test_some_and_store("results/mcts_101", "dataset-assignment2/data/", "101", 100, MCTS, n_expansions=20)


if __name__ == "__main__":
    main()