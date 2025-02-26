import numpy as np
import random
import tsplib95
import itertools


# Set seed for reproducibility
np.random.seed(42)
random.seed(42)

# Generate a set of cities
#num_cities = 10
#cities = np.random.rand(num_cities, 2)

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


# Function to create a random initial route
def create_initial_route(cities):
    return random.sample(list(cities), len(cities))

# Function to create neighboring solutions
def get_neighbors(route):
    neighbors = []
    for i in range(len(route)):
        for j in range(i + 1, len(route)):
            neighbor = route.copy()
            neighbor[i], neighbor[j] = neighbor[j], neighbor[i]
            neighbors.append(neighbor)
    return neighbors

def hill_climbing(cities, graph):
    current_route = create_initial_route(cities)
    current_distance = calculate_cost(current_route, graph)

    while True:
        neighbors = get_neighbors(current_route)
        next_route = min(neighbors, key= lambda x: calculate_cost(x,graph))
        next_distance = calculate_cost(next_route, graph)
        
        if next_distance >= current_distance:
            break
        
        current_route, current_distance = next_route, next_distance

    return current_route, current_distance
    

# Set name of file
if __name__ == "__main__":
    filename = "/Users/dyl/Desktop/TSP/tsplib-master/berlin52.tsp"  # Replace with your TSP file path
    cities, graph = load_tsp_file(filename)
    best_route, best_distance = hill_climbing(cities, graph)
    print("Best Route: " , best_route)
    print("Total Cost: ", best_distance)