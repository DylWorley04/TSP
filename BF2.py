import tsplib95
import itertools
import time
import networkx as nx
import matplotlib.pyplot as plt

begin = time.time()

# Function to load a TSPLIB file and extract cities and distances
def load_tsp_file(filename):
    problem = tsplib95.load(filename)
    cities = list(problem.get_nodes())
    graph = {i: {j: problem.get_weight(i, j) for j in cities} for i in cities}
    G = problem.get_graph()

    # Draw the graph
    pos = nx.spectral_layout(G)  # Use a layout algorithm to position nodes
    nx.draw(G, pos, with_labels=True, node_size=300, node_color='lightblue', font_size=10, font_weight='bold', edge_color='gray')
    
    # Draw edge labels (weights)
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    return cities, graph

# Function to calculate the total cost of a route
def calculate_cost(route, graph):
    total_cost = 0
    n = len(route)
    for i in range(n):
        current_city = route[i]
        next_city = route[(i + 1) % n]  # Wrap around to the start of the route
        total_cost += graph[current_city][next_city]
    return total_cost

# Main function to solve TSP using brute force
def tsp_brute_force(filename):
    # Load the TSP file
    cities, graph = load_tsp_file(filename)

    # Generate all permutations of the cities (excluding the starting city)
    start_city = cities[0]
    remaining_cities = [city for city in cities if city != start_city]
    all_permutations = itertools.permutations(remaining_cities)

    # Initialize variables to track the minimum cost and corresponding route
    min_cost = float('inf')
    optimal_route = None

    # Iterate over all permutations and calculate costs
    for perm in all_permutations:
        route = (start_city,) + perm + (start_city,)  # Add start city at the beginning and end
        cost = calculate_cost(route, graph)
        if cost < min_cost:
            min_cost = cost
            optimal_route = route

    time.sleep(1)
    end = time.time()
    # Print the optimal route and its cost
    print(f"Optimal Route: {optimal_route}")
    print(f"Total Cost: {min_cost}")
    print(f"Total runtime of the program is {end - begin}")
    #plt.show()

# Set name of file
if __name__ == "__main__":
    filename = "/Users/dyl/Desktop/TSP/tsplib-master/d4.tsp"  # Replace with your TSP file path
    tsp_brute_force(filename)