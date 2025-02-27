import tsplib95
import itertools

def load_tsp_file(filename): #function to define file name
    problem = tsplib95.load(filename) #loads file into problem variable
    cities = list(problem.get_nodes()) #gets all the nodes storing thme in the cities variables
    graph = {i: {j: problem.get_weight(i, j) for j in cities} for i in cities}
    return cities, graph #returns variables for cities and graph

def tsp_nearest_neighbour(graph, cities): #defines function for nearest neighbour algorithm
    num_cities = len(cities) #gets the number of cities from the tsp file and then stores it in variable
    start_city = cities[0] 
    unvisited_cities = set(cities)  
    unvisited_cities.remove(start_city) 
    
    current_city = start_city #starts at start city
    path = [start_city] 
    total_cost = 0 

    while unvisited_cities: #while there are unvisited cities
        nearest_city = min(unvisited_cities, key=lambda city: graph[current_city][city]) #creates a temporary variable called lambda and sets it to the nearest city
        total_cost += graph[current_city][nearest_city] 
        path.append(nearest_city) 
        unvisited_cities.remove(nearest_city) 
        current_city = nearest_city 

    # Return to the starting city
    total_cost += graph[current_city][start_city] 
    path.append(start_city)

    return path, total_cost

if __name__ == "__main__": #main function
    filename = "./tsplib-master/berlin52.tsp" 
    cities, graph = load_tsp_file(filename) 

    best_path, min_cost = tsp_nearest_neighbour(graph, cities) 
    print("Best path: ", best_path) 
    print("Minimum cost: ", min_cost)