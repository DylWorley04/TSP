import numpy as np
import networkx as nx
from scipy.sparse.csgraph import minimum_spanning_tree
from scipy.spatial.distance import pdist, squareform
import tsplib95

def christofides(tsp_file):
    # Load the TSP problem from the file
    problem = tsplib95.load(tsp_file)
    nodes = list(problem.get_nodes())
    n = len(nodes)
    
    # Create a distance matrix
    coords = [problem.node_coords[node] for node in nodes]
    dist_matrix = squareform(pdist(coords, metric='euclidean'))
    
    # Step 1: Find the Minimum Spanning Tree (MST)
    mst = minimum_spanning_tree(dist_matrix)
    mst = mst.toarray()
    
    # Step 2: Find nodes with odd degree in the MST
    odd_degree_nodes = [i for i in range(n) if np.sum(mst[i] > 0) % 2 != 0]
    
    # Step 3: Find the minimum weight perfect matching for the odd degree nodes
    subgraph = dist_matrix[np.ix_(odd_degree_nodes, odd_degree_nodes)]
    G = nx.Graph(subgraph)
    matching = nx.min_weight_matching(G, maxcardinality=True)
    
    # Step 4: Combine the MST and the matching to form a multigraph
    multigraph = np.copy(mst)
    for (u, v) in matching:
        multigraph[odd_degree_nodes[u], odd_degree_nodes[v]] = dist_matrix[odd_degree_nodes[u], odd_degree_nodes[v]]
        multigraph[odd_degree_nodes[v], odd_degree_nodes[u]] = dist_matrix[odd_degree_nodes[v], odd_degree_nodes[u]]
    
    # Step 5: Find an Eulerian circuit in the multigraph
    G = nx.from_numpy_array(multigraph)
    eulerian_circuit = list(nx.eulerian_circuit(G))
    
    # Step 6: Convert the Eulerian circuit to a Hamiltonian cycle by skipping repeated nodes
    visited = set()
    hamiltonian_cycle = []
    for (u, v) in eulerian_circuit:
        if u not in visited:
            hamiltonian_cycle.append(u)
            visited.add(u)
    hamiltonian_cycle.append(hamiltonian_cycle[0])
    
    # Calculate the total cost of the Hamiltonian cycle
    total_cost = sum(dist_matrix[hamiltonian_cycle[i], hamiltonian_cycle[i+1]] for i in range(len(hamiltonian_cycle)-1))
    
    return hamiltonian_cycle, total_cost

# Example usage
tsp_file = "/Users/dyl/Desktop/TSP/tsplib-master/att8.tsp"
cycle, cost = christofides(tsp_file)
print("Hamiltonian Cycle:", cycle)
print("Total Cost:", cost)