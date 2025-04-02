import tsplib95
import heapq
import time
import matplotlib.pyplot as plt

def load_tsp_file(filename):
    """Load TSP file and return cities, graph, and problem object"""
    problem = tsplib95.load(filename)
    cities = list(problem.get_nodes())
    graph = {i: {j: problem.get_weight(i, j) for j in cities} for i in cities}
    return cities, graph, problem

def create_adjacency_list(graph, cities):
    """Convert graph dictionary to adjacency list format"""
    n = len(cities)
    adj = [[] for _ in range(n)]
    
    for i in cities:
        for j in cities:
            if i != j:
                adj[i-1].append([j-1, graph[i][j]])  # Convert to 0-based indexing
    return adj

def tour_cost(tour, graph):
    """Calculate the total cost of a tour"""
    cost = 0
    for i in range(len(tour)-1):
        cost += graph[tour[i]+1][tour[i+1]+1]  # Convert back to 1-based for graph lookup
    return cost

def eulerian_circuit(adj, u, tour, visited, parent):
    """Find Eulerian circuit using DFS"""
    visited[u] = True
    tour.append(u)
 
    for neighbor in adj[u]:
        v = neighbor[0]
        if v == parent:
            continue
        
        if not visited[v]:
            eulerian_circuit(adj, v, tour, visited, u)

def find_mst(adj, mst_cost):
    """Find minimum spanning tree using Prim's algorithm"""
    n = len(adj)
    visited = [False] * n
    mst_edges = []
    pq = []
    heapq.heappush(pq, [0, 0, -1])
 
    while pq:
        current = heapq.heappop(pq)
        u = current[1]
        weight = current[0]
        parent = current[2]
 
        if visited[u]:
            continue
 
        mst_cost[0] += weight
        visited[u] = True
 
        if parent != -1:
            mst_edges.append([u, parent, weight])
 
        for neighbor in adj[u]:
            v = neighbor[0]
            if v == parent:
                continue
            w = neighbor[1]
 
            if not visited[v]:
                heapq.heappush(pq, [w, v, u])
    return mst_edges

def approximate_tsp(adj, graph, cities):
    """Approximate TSP solution using MST and Eulerian circuit"""
    n = len(adj)
    mst_cost = [0]
    mst_edges = find_mst(adj, mst_cost)
 
    visited = [False] * n
    mst_adj = [[] for _ in range(n)]
    
    for e in mst_edges:
        mst_adj[e[0]].append([e[1], e[2]])
        mst_adj[e[1]].append([e[0], e[2]])
 
    tour = []
    eulerian_circuit(mst_adj, 0, tour, visited, -1)
    tour.append(0)  # Return to start
 
    # Remove duplicates while maintaining order
    seen = set()
    unique_tour = []
    for city in tour:
        if city not in seen:
            seen.add(city)
            unique_tour.append(city)
    unique_tour.append(0)  # Complete the cycle
    
    return unique_tour

def plot_route(tour, problem):
    """Plot the TSP route"""
    city_coords = problem.node_coords
    
    # Convert tour indices back to original node numbers
    original_tour = [city+1 for city in tour]
    
    route_coords = [city_coords[city] for city in original_tour]
    route_x = [x for x, y in route_coords]
    route_y = [y for x, y in route_coords]
    
    plt.figure(figsize=(10, 8))
    plt.plot(route_x, route_y, 'r-', marker='o', markersize=5, label="Route")
    plt.title("Approximate TSP Route (MST-based)")
    plt.xlabel("X-coordinate")
    plt.ylabel("Y-coordinate")
    plt.grid(True)
    plt.legend()
    plt.show()

def tsp(filename):
    """Main function to solve TSP using approximation algorithm"""
    start_time = time.time()
    
    # Load TSP file
    cities, graph, problem = load_tsp_file(filename)
    
    # Create adjacency list (0-based indexing)
    adj = create_adjacency_list(graph, cities)
    
    # Solve TSP
    tour = approximate_tsp(adj, graph, cities)
    
    # Calculate cost (convert back to 1-based for graph lookup)
    cost = tour_cost(tour, graph)
    
    end_time = time.time()
    
    print(f"Approximate TSP Tour: {[city+1 for city in tour]}")  # Convert back to 1-based for output
    print(f"Approximate Tour Cost: {cost}")
    print(f"Execution Time: {end_time - start_time:.4f} seconds")
    
    # Plot the route
    plot_route(tour, problem)
    
    return cost

if __name__ == "__main__":
    filename = "./tsplib-master/berlin52.tsp"  # Change to your TSP file path
    tsp(filename)