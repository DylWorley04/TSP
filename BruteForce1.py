import tsplib95
from itertools import permutations

def load_tsp_file(filename):
    problem = tsplib95.load(filename)

    cities = list(problem.get_nodes())
    graph = {i: {j: problem.get_weight(i,j) for j in cities} for i in cities}
    return cities, graph

def tsp_brute_force(graph, cities):
    num_cities = len(cities)
    min_cost = float('inf')
    best_path = None

    start_city = cities[0]
    remaining_cities = [city for city in cities if city != start_city]

    for perm in permutations(remaining_cities):
        path = [start_city] + list(perm) + [start_city]
        cost = sum(graph[path[i]][path[i+1]] for i in range(num_cities))

        if cost < min_cost:
            min_cost = cost
            best_path = path

    return best_path, min_cost

if __name__ == "__main__":
    filename = "/Users/dyl/Desktop/TSP/tsplib-master/att8.tsp"
    cities, graph = load_tsp_file(filename)

    best_path, min_cost = tsp_brute_force(graph, cities)
    print("Best path: ", best_path)
    print("Minimum cost: ", min_cost)
