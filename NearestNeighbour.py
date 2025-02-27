import tsplib95
import itertools
import matplotlib.pyplot as plt

def load_tsp_file(filename): #function to define file name
    problem = tsplib95.load(filename) #loads file into problem variable
    cities = list(problem.get_nodes()) #gets all the nodes storing thme in the cities variables
    graph = {i: {j: problem.get_weight(i, j) for j in cities} for i in cities}
    return cities, graph, problem #returns variables for cities and graph

def tsp_nearest_neighbour(graph, cities): #defines function for nearest neighbour algorithm
    num_cities = len(cities) #gets the number of cities from the tsp file and then stores it in variable
    start_city = cities[0] 
    unvisited_cities = set(cities)  
    unvisited_cities.remove(start_city) 
    
    current_city = start_city #starts at start city
    path = [start_city] 
    total_cost = 0 

    while unvisited_cities: #while there are unvisited cities
        nearest_city = min(unvisited_cities, key=lambda city: graph[current_city][city])
 #creates a temporary variable called lambda and sets it to the nearest city
        total_cost += graph[current_city][nearest_city] 
        path.append(nearest_city) 
        unvisited_cities.remove(nearest_city) 
        current_city = nearest_city 

    # Return to the starting city
    total_cost += graph[current_city][start_city] 
    path.append(start_city)

    return path, total_cost

# Function to plot the route using matplotlib
def plot_route(cities, route, problem):
    # Get the coordinates of the cities from the problem
    city_coords = problem.node_coords

    # Plot cities as red dots
    plt.figure(figsize=(10, 8))
    for city, (x, y) in city_coords.items():
        plt.scatter(x, y, color='red', zorder=5)
        plt.text(x + 20, y + 20, str(city), fontsize=12, color='black')

    # Plot the route
    route_coords = [city_coords[city] for city in route]
    route_x = [x for x, y in route_coords]
    route_y = [y for x, y in route_coords]
    
    # Add the return to the starting city to complete the loop
    route_x.append(route_x[0])
    route_y.append(route_y[0])

    plt.plot(route_x, route_y, 'b-', marker='o', markersize=10, label="Route")
    plt.title("TSP Route")
    plt.xlabel("X-coordinate")
    plt.ylabel("Y-coordinate")
    plt.grid(False)
    plt.legend()
    plt.show()

if __name__ == "__main__": #main function
    filename = "./tsplib-master/att48.tsp" 
    cities, graph, problem = load_tsp_file(filename) 

    best_path, min_cost = tsp_nearest_neighbour(graph, cities) 
    print("Best path: ", best_path) 
    print("Minimum cost: ", min_cost)
    plot_route(cities, best_path, problem)