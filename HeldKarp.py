import tsplib95
import math
import time
import matplotlib.pyplot as plt

# Function to load a TSPLIB file, extracting both distance matrix and problem data
def load_tsp_file(filename):
    problem = tsplib95.load(filename)
    cities = list(problem.get_nodes())
    num_cities = len(cities)
    distance_matrix = [[problem.get_weight(cities[i], cities[j]) for j in range(num_cities)] for i in range(num_cities)]
    return problem, cities, distance_matrix

# Function to solve TSP using dynamic programming
def tsp_dynamic_programming(filename):
    problem, cities, distances = load_tsp_file(filename)

    n = len(distances)
    dp = [[math.inf] * n for _ in range(1 << n)]
    parent = [[None] * n for _ in range(1 << n)]

    dp[1][0] = 0

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

    min_cost = math.inf
    end_city = None
    full_mask = (1 << n) - 1
    for last in range(1, n):
        cost = dp[full_mask][last] + distances[last][0]
        if cost < min_cost:
            min_cost = cost
            end_city = last

    tour = []
    mask = full_mask
    last = end_city
    while last is not None:
        tour.append(cities[last])
        new_last = parent[mask][last]
        mask ^= (1 << last)
        last = new_last

    tour = tour[::-1]
    tour.append(cities[0])
    
    return problem, cities, tour, min_cost

# Function to plot the route using matplotlib
def plot_route(cities, route, problem):
    city_coords = problem.node_coords

    route_coords = [city_coords[city] for city in route]
    route_x = [x for x, y in route_coords]
    route_y = [y for x, y in route_coords]

    plt.figure(figsize=(8, 6))
    plt.plot(route_x, route_y, 'r-', marker='o', markersize=7, label="Optimal Route")
    
    for city in cities:
        x, y = city_coords[city]
        plt.scatter(x, y, color='blue')
        plt.text(x, y, str(city), fontsize=12, color='black', ha='right')

    plt.title("TSP Optimal Route")
    plt.xlabel("X-coordinate")
    plt.ylabel("Y-coordinate")
    plt.grid(True)
    plt.legend()
    plt.show()

# Main execution
if __name__ == "__main__":
    filename = "/Users/dyl/Desktop/TSP/tsplib-master/att8.tsp"

    start_time = time.time()
    problem, cities, best_path, min_cost = tsp_dynamic_programming(filename)
    end_time = time.time()

    print("Best path:", best_path)
    print("Minimum cost:", min_cost)
    print("Execution time:", (end_time - start_time), "seconds")

    plot_route(cities, best_path, problem)
