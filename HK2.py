import tsplib95
import math
import time
import networkx as nx
import matplotlib.pyplot as plt

# Function to load a TSPLIB file and extract the distance matrix
def load_tsp_file(filename):
    # Load the TSP file
    problem = tsplib95.load(filename)
    # Extract the list of cities/nodes
    cities = list(problem.get_nodes())
    # Construct the distance matrix
    num_cities = len(cities)
    distance_matrix = [[0] * num_cities for _ in range(num_cities)]

    for i in range(num_cities):
        for j in range(num_cities):
            distance_matrix[i][j] = problem.get_weight(cities[i], cities[j])

    return distance_matrix


# Main function to solve TSP using dynamic programming
def tsp_dynamic_programming(filename):
    # Load the TSP file and get the distance matrix
    distances = load_tsp_file(filename)

    n = len(distances)  # Number of cities
    dp = [[math.inf] * n for _ in range(1 << n)]
    parent = [[None] * n for _ in range(1 << n)]

    # Base case: starting from city 0
    dp[1][0] = 0

    # Fill DP table
    for mask in range(1 << n):
        for last in range(n):
            if not (mask & (1 << last)):
                continue
            for next in range(n):
                if mask & (1 << next):
                    continue
                new_mask = mask | (1 << next)
                new_dist = dp[mask][last] + distances[last][next]
                if new_dist < dp[new_mask][next]:
                    dp[new_mask][next] = new_dist
                    parent[new_mask][next] = last

    # Find the optimal tour and minimum cost
    min_cost = math.inf
    end_city = None
    full_mask = (1 << n) - 1

    for last in range(1, n):
        cost = dp[full_mask][last] + distances[last][0]
        if cost < min_cost:
            min_cost = cost
            end_city = last

    # Reconstruct the optimal tour
    tour = []
    mask = full_mask
    last = end_city
    while mask:
        tour.append(last)
        new_last = parent[mask][last]
        mask ^= (1 << last)
        last = new_last
    tour = tour[::-1]
    tour.append(0)  # Add the starting city at the end to complete the loop

    # Print the final dp table values
    #print("Final DP Table:")
    #for mask in range(1 << n):
        #print(f"mask = {mask:04b}: {dp[mask]}")

    # Print the optimal tour and minimum cost
    print("\nOptimal Tour:", tour)
    print("Minimum Cost:", min_cost)

# Set name of file
if __name__ == "__main__":
    filename = "/Users/dyl/Desktop/TSP/tsplib-master/berlin52.tsp"  # Replace with your TSP file path
    tsp_dynamic_programming(filename)