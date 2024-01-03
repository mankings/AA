import matplotlib.pyplot as plt
import networkx as nx
import json
import sys

def visualize_graph_from_file(filepath):
    # Read the graph from the file
    with open(filepath, 'r') as file:
        adjacency_list = json.load(file)
    
    # Create a new graph from the adjacency list
    G = nx.Graph()
    for node, neighbors in adjacency_list.items():
        node = tuple(map(int, node.strip('()').split(', ')))
        G.add_node(node)  # Add the node
        for neighbor in neighbors:
            neighbor = tuple(map(int, neighbor.strip('()').split(', ')))
            G.add_edge(node, neighbor)
    
    # Calculate graph information
    num_vertices = G.number_of_nodes()
    num_edges = G.number_of_edges()
    max_edges = num_vertices * (num_vertices - 1) // 2
    edge_percent = num_edges / max_edges if max_edges > 0 else 0

    # Draw the graph
    pos = {node: (node[0], node[1]) for node in G.nodes()}  # Position is the same as the node label
    nx.draw(G, pos, with_labels=True, node_size=500, node_color='lightblue', linewidths=0.25, font_size=8)
    
    # Add the graph information label
    plt.text(0.05, 0.95, f'Vertices: {num_vertices}\nEdges: {num_edges}\nEdge percent: {edge_percent:.2%}\nMax edges: {max_edges}',
             transform=plt.gca().transAxes, fontsize=10, verticalalignment='top')

    plt.show()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python graph_display.py <graph_file.json>")
        sys.exit(1)
    
    graph_file = sys.argv[1]
    visualize_graph_from_file(graph_file)
