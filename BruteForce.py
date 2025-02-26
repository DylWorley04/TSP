import tsplib95
import numpy as np
import random
import itertools


# Function to load a TSPLIB file and extract cities and distances
def load_tsp_file(filename):
    problem = tsplib95.load(filename)
    cities = list(problem.get_nodes())
    graph = {i: {j: problem.get_weight(i, j) for j in cities} for i in cities}
    G = problem.get_graph()
    return cities, graph

def calculate_cost(route, graph):
    total_cost = 0
    n = len(route)
    for i in range(n):
        current_city = route[i]
        next_city = route[(i + 1) % n]  # Wrap around to the start of the route
        total_cost += graph[current_city][next_city]
    return total_cost

def brute_force(cities, graph):
    # Generate all permutations of the cities
    all_permutations = itertools.permutations(cities)

    # Initialize variables to track the minimum cost and corresponding route
    min_cost = float('inf')
    optimal_route = None

    # Iterate over all permutations and calculate costs
    for perm in all_permutations:
        cost = calculate_cost(perm, graph)
        if cost < min_cost:
            min_cost = cost
            optimal_route = perm

    return optimal_route, min_cost

# Set name of file
if __name__ == "__main__":
    filename = "/Users/dyl/Desktop/TSP/tsplib-master/att8.tsp"  # Replace with your TSP file path
    cities, graph = load_tsp_file(filename)
    best_route, best_distance = brute_force(cities, graph)
    print("Best Route: " , best_route)
    print("Total Cost: ", best_distance)