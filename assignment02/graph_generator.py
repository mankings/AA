import random
import networkx as nx
import os
import sys
import json

seed = 103341
random.seed(seed)

def generate_vertex(existing_vertices):
    while True:
        x, y = random.randint(1, 100), random.randint(1, 100)
        if all((x - ex)**2 + (y - ey)**2 >= 4 for ex, ey in existing_vertices):
            return (x, y)

def generate_graph(num_vertices, edge_percent):
    G = nx.Graph()
    vertices = []
    for _ in range(num_vertices):
        new_vertex = generate_vertex(vertices)
        vertices.append(new_vertex)
        G.add_node(new_vertex)

    max_edges = num_vertices * (num_vertices - 1) // 2
    num_edges = int(max_edges * edge_percent)
    all_possible_edges = [(vertices[i], vertices[j]) for i in range(num_vertices) for j in range(i+1, num_vertices)]
    edges = random.sample(all_possible_edges, num_edges)
    G.add_edges_from(edges)

    return G

def save_graph(G, filename):
    adjacency_list = {str(node): [str(neighbor) for neighbor in G.neighbors(node)] for node in G.nodes()}
    with open(filename, 'w') as file:
        json.dump(adjacency_list, file, indent=4)

def generate_and_save_graphs(sizes, edge_percents, folder):
    if os.path.exists(folder):
        os.system(f"rm {folder}/graph_*.json")
    else:
        os.makedirs(folder)
    

    for size in sizes:
        for edge_percent in edge_percents:
            G = generate_graph(size, edge_percent)
            filename = os.path.join(folder, f'graph_{str(size).zfill(3)}_{int(edge_percent*100)}.json')
            save_graph(G, filename)

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print("Usage: python graph_generator.py <min_size> <max_size> <step>")
        sys.exit(1)

    min_size = int(sys.argv[1])
    max_size = int(sys.argv[2])
    step = int(sys.argv[3])

    if min_size > max_size:
        print("Error: min_size should be less than or equal to max_size")
        sys.exit(1)

    sizes = range(min_size, max_size + 1, step)
    edge_percents = [0.125, 0.25, 0.5, 0.75]
    folder = 'graphs/graphs'
    generate_and_save_graphs(sizes, edge_percents, folder)