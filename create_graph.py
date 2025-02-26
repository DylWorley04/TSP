def load_tsp_file(filename):
    problem = tsplib95.load(filename)
    cities = list(problem.get_nodes())
    graph = {i: {j: problem.get_weight(i, j) for j in cities} for i in cities}
    G = problem.get_graph()

    # Draw the graph
    pos = nx.spectral_layout(G)  # Use a layout algorithm to position nodes
    nx.draw(G, pos, with_labels=True, node_size=300, node_color='lightblue', font_size=10, font_weight='bold', edge_color='gray')
    
    # Draw edge labels (weights)
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    return cities, graph

def drawGraph(filename, problem):
    # get problem and create graph
    G = problem.get_graph()
    # draw graph
    pos = nx.spectral_layout(G)
    nx.draw(G, pos, with_labels=True, node_size=300, node_color='lightblue', font_size=10, font_weight='bold', edge_color='gray')
    #draw edge labels
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    #display graph
    plt.show