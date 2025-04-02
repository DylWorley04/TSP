import numpy as np
import tsplib95
import matplotlib.pyplot as plt

#np.random.seed(42)

# Load TSPLIB file using tsplib95
def load_tsp_file(filename):
    problem = tsplib95.load(filename)
    cities = list(problem.get_nodes())
    adj_matrix = np.array([[problem.get_weight(i, j) for j in cities] for i in cities])
    return adj_matrix, cities, problem

# Branch and Bound Functions
def first_min(adj, i): #finds the first minimum edge distance from i to any other node
    min_val = np.inf
    for k in range(len(adj)):
        if adj[i][k] < min_val and i != k:
            min_val = adj[i][k]
    return min_val

def second_min(adj, i): #finds the second minimum edge distance from i to any other node
    first, second = np.inf, np.inf
    for j in range(len(adj)):
        if i == j:
            continue
        if adj[i][j] <= first:
            second = first
            first = adj[i][j]
        elif adj[i][j] <= second:
            second = adj[i][j]
    return second

def tsp_rec(adj, current_bound, current_weight, level, current_path, visited, final_res, final_path): #recursive function to solve by pruning branches
    N = len(adj) 

    if level == N:
        if adj[current_path[level - 1]][current_path[0]] != 0:
            current_res = current_weight + adj[current_path[level - 1]][current_path[0]]
            if current_res < final_res[0]:
                final_path[:N + 1] = current_path[:]
                final_path[N] = current_path[0]
                final_res[0] = current_res
        return

    for i in range(N):
        if adj[current_path[level-1]][i] != 0 and not visited[i]:
            temp = current_bound
            current_weight += adj[current_path[level - 1]][i]

            if level == 1:
                current_bound -= (first_min(adj, current_path[level - 1]) + first_min(adj, i)) / 2
            else:
                current_bound -= (second_min(adj, current_path[level - 1]) + first_min(adj, i)) / 2

            if current_bound + current_weight < final_res[0]:
                current_path[level] = i
                visited[i] = True

                tsp_rec(adj, current_bound, current_weight, level + 1, current_path, visited, final_res, final_path)

            current_weight -= adj[current_path[level - 1]][i]
            current_bound = temp

            visited = [False] * N
            for j in range(level):
                if current_path[j] != -1:
                    visited[current_path[j]] = True

# Main TSP solver using Branch and Bound
def solve_tsp_branch_bound(adj):
    N = len(adj)
    current_bound = 0
    current_path = [-1] * (N + 1)
    visited = [False] * N

    final_res = [np.inf]
    final_path = [-1] * (N + 1)

    for i in range(N):
        current_bound += (first_min(adj, i) + second_min(adj, i))

    current_bound = np.ceil(current_bound / 2)

    visited[0] = True
    current_path[0] = 0

    tsp_rec(adj, current_bound, 0, 1, current_path, visited, final_res, final_path)
    return final_res[0], final_path

# Plotting the solution using matplotlib
def plot_route(problem, path):
    city_coords = problem.node_coords
    coords = np.array([city_coords[city + 1] for city in path])

    plt.figure(figsize=(10, 8))
    plt.scatter(coords[:, 0], coords[:, 1], color='red', zorder=5)
    for i, city in enumerate(path[:-1]):
        plt.text(coords[i, 0], coords[i, 1], str(city + 1), fontsize=10)

    plt.plot(coords[:, 0], coords[:, 1], 'b-', marker='o', markersize=5)
    plt.title("Optimal TSP Route (Branch and Bound)")
    plt.xlabel("X-coordinate")
    plt.ylabel("Y-coordinate")
    plt.grid(True)
    plt.show()

# Example usage
if __name__ == "__main__":
    filename = "/Users/dyl/Desktop/TSP/tsplib-master/att8.tsp"  # Replace with your TSP file path 
    adj_matrix, cities, problem = load_tsp_file(filename)

    best_cost, best_route = solve_tsp_branch_bound(adj_matrix)

    print("Minimum Cost:", best_cost)
    print("Optimal Path:", [cities[i] for i in best_route])

    plot_route(problem, best_route)
