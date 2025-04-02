import tsplib95
import numpy as np
import random
import itertools
import matplotlib.pyplot as plt
import time

begin_time = time.time()

# Function to load a TSPLIB file and extract cities and distances
def load_tsp_file(filename):
    problem = tsplib95.load(filename)
    cities = list(problem.get_nodes())
    graph = {i: {j: problem.get_weight(i, j) for j in cities} for i in cities}
    G = problem.get_graph()
    return cities, graph, problem

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
end_time = time.time()

# Function to plot the route using matplotlib
def plot_route(cities, route, problem):
    # Get the coordinates of the cities from the problem
    city_coords = problem.node_coords

    # Plot cities as red dots
    #plt.figure(figsize=(10, 8))
    #for city, (x, y) in city_coords.items():
        #plt.scatter(x, y, color='red', zorder=5)
        #plt.text(x + 20, y + 20, str(city), fontsize=12, color='black')

    # Plot the route
    route_coords = [city_coords[city] for city in route]
    route_x = [x for x, y in route_coords]
    route_y = [y for x, y in route_coords]
    
    # Add the return to the starting city to complete the loop
    route_x.append(route_x[0])
    route_y.append(route_y[0])

    plt.plot(route_x, route_y, 'r-', marker='o', markersize=5, label="Route")
    plt.title("TSP Route")
    plt.xlabel("X-coordinate")
    plt.ylabel("Y-coordinate")
    plt.grid(False)
    plt.legend()
    plt.show()

# Set name of file
if __name__ == "__main__":
    filename = "/Users/dyl/Desktop/TSP/tsplib-master/att8.tsp"  # Replace with your TSP file path
    cities, graph, problem = load_tsp_file(filename)
    best_route, best_distance = brute_force(cities, graph)
    print("Best Route: " , best_route)
    print("Number of Cities: ", len(best_route))
    print("Total Cost: ", best_distance)
    print("Execution Time: ", ((end_time - begin_time)))
    # Plot the best route
    plot_route(cities, best_route, problem)