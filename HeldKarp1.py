import tsplib95

def load_tsp_file(filename):
    """
    Load a TSP problem from a TSPLIB file and convert it into:
      - A list of city labels (e.g., [1, 2, 3, ...]).
      - A dictionary 'graph' where graph[u][v] gives the distance from city u to city v.
    """
    problem = tsplib95.load(filename)
    
    # Extract node labels (cities)
    cities = list(problem.get_nodes())
    cities.sort()  # sort to ensure consistent order if needed

    # Build a dictionary-of-dictionaries for distances
    graph = {}
    for c1 in cities:
        graph[c1] = {}
        for c2 in cities:
            graph[c1][c2] = problem.get_weight(c1, c2)
    
    return cities, graph

def tsp_bitmask_dp(dist):
    """
    Given a 1-based dist matrix:
      dist[i][j] = cost of traveling from i to j,
    solve TSP using bitmask DP.
    """
    n = len(dist) - 1  # if dist is (n+1) x (n+1), then there are n cities
    # Prepare memo table for top-down recursion
    # memo[i][mask] = -1 means not computed yet
    memo = [[-1] * (1 << (n + 1)) for _ in range(n + 1)]
    
    def fun(i, mask):
        """
        Returns the cost of completing the tour starting from city 1, 
        visiting all cities in mask, and currently at city i.
        """
        # Base case: if mask == ((1 << i) | 3), we have only city 1 and city i visited
        # This means all other cities have been visited, 
        # so just return distance from i back to 1.
        if mask == ((1 << i) | 3):
            return dist[1][i]

        if memo[i][mask] != -1:
            return memo[i][mask]

        res = 10**9
        # Try traveling through any city j that is in mask (visited) 
        # and not city i or city 1
        for j in range(1, n + 1):
            if (mask & (1 << j)) != 0 and j != i and j != 1:
                # Recur: remove i from the mask, then add cost of j->i
                cost = fun(j, mask & (~(1 << i))) + dist[j][i]
                if cost < res:
                    res = cost
        
        memo[i][mask] = res
        return res

    ans = 10**9
    all_visited_mask = (1 << (n + 1)) - 1  # mask with all cities visited (for 1..n)
    
    # Try finishing the tour at each city i, then add cost from i->1
    for i in range(1, n + 1):
        cost = fun(i, all_visited_mask) + dist[i][1]
        ans = min(ans, cost)
    
    return ans

if __name__ == "__main__":
    # 1. Specify your TSPLIB file
    filename = "/Users/dyl/Desktop/TSP/tsplib-master/att8.tsp"
    
    # 2. Load TSP data (cities, graph)
    cities, graph = load_tsp_file(filename)
    n = len(cities)
    
    # 3. Create a 1-based dist matrix for our bitmask DP
    #    NOTE: Ensure that city labels are 1..n for this code to work directly.
    #    If the TSPLIB file labels differ, we'll map them to 1..n.
    
    # -- Check if the TSPLIB nodes are exactly 1..n:
    #    If not, build a mapping to re-index them.
    expected_labels = list(range(1, n+1))
    
    if cities != expected_labels:
        # Build a map from the original labels to 1..n
        label_to_one_based = {}
        for idx, city_label in enumerate(cities, start=1):
            label_to_one_based[city_label] = idx
        
        # Create dist matrix of size (n+1) x (n+1)
        dist = [[0]*(n+1) for _ in range(n+1)]
        for c1 in cities:
            for c2 in cities:
                i = label_to_one_based[c1]
                j = label_to_one_based[c2]
                dist[i][j] = graph[c1][c2]
    else:
        # The city labels are already 1..n
        dist = [[0]*(n+1) for _ in range(n+1)]
        for i in range(1, n+1):
            for j in range(1, n+1):
                dist[i][j] = graph[i][j]
    
    # 4. Run the bitmask DP TSP
    min_cost = tsp_bitmask_dp(dist)
    
    print("Number of cities:", n)
    print("The cost of the most efficient tour =", min_cost)
