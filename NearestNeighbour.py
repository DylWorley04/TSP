import tsplib95
import itertools

def load_tsp_file(filename): #function to define file name
    problem = tsplib95.load(filename) #loads file into problem variable
    cities = list(problem.get_nodes()) #gets all the nodes storing thme in the cities variables
    graph = {i: {j: problem.get_weight(i, j) for j in cities} for i in cities}
    return cities, graph #returns variables for cities and graph

def tsp_nearest_neighbour(graph, cities): #defines function for nearest neighbour algorithm
    num_cities = len(cities) #gets the number of cities from the tsp file and then stores it in variable
    start_city = cities[0] #sets the start city at start of problem
    unvisited_cities = set(cities) #number of univistited cities 
    unvisited_cities.remove(start_city) #removes the start city from the list of unvisited cities
    
    current_city = start_city #starts at start city
    path = [start_city] 
    total_cost = 0 #defines total cost and set to 0

    while unvisited_cities: #while there are unvisited cities
        nearest_city = min(unvisited_cities, key=lambda city: graph[current_city][city]) #creates a temporary variable called lambda and sets it to the nearest city
        total_cost += graph[current_city][nearest_city] #adds the cost of the nearest city to the total cost
        path.append(nearest_city) #amends the path to include the nearest city
        unvisited_cities.remove(nearest_city) #removes the nearest city from the list of unvisited cities
        current_city = nearest_city #sets the current city to the previous nerest city

    # Return to the starting city
    total_cost += graph[current_city][start_city] #adds the current city to the total cost
    path.append(start_city)

    return path, total_cost

if __name__ == "__main__": #main function
    filename = "./tsplib-master/berlin52.tsp" #load a tsp file using local file path
    cities, graph = load_tsp_file(filename) #stores current file path in filename variable

    best_path, min_cost = tsp_nearest_neighbour(graph, cities) #assigns the best path and minimum cost to the graph and citites values
    print("Best path: ", best_path) #prints best path
    print("Minimum cost: ", min_cost)#prints minimum cost