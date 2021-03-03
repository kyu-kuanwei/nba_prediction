from data_pipeline import DataPipeline
from ortools.algorithms import pywrapknapsack_solver
import pandas as pd

def recommand():
    # Create the solver.
    solver = pywrapknapsack_solver.KnapsackSolver(
        pywrapknapsack_solver.KnapsackSolver.
        KNAPSACK_MULTIDIMENSION_SCIP_MIP_SOLVER, 'KnapsackExample')

    valid_players = DataPipeline().valid_players

    values = valid_players['SCR'].tolist()
    weights = [valid_players['RATING'].tolist()]
    capacities = [430]

    solver.Init(values, weights, capacities)
    computed_value = solver.Solve()

    packed_items = []
    packed_weights = []
    total_weight = 0
    # print('Total value =', computed_value)
    for i in range(len(values)):
        if solver.BestSolutionContains(i):
            packed_items.append(i)
            packed_weights.append(weights[0][i])
            total_weight += weights[0][i]
    print('Total weight:', total_weight)

    print('Total_Scores:', valid_players.iloc[packed_items]['SCR'].sum())
    print(valid_players.iloc[packed_items])